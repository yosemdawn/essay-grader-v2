import base64
import json
import logging
import re
from typing import Any, Dict, List

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings
from app.services.teacher_config import teacher_config_service

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


GRADING_PROMPT_TEMPLATE = """
你是一名专业的作文批改老师，能够同时批改中文作文和英文作文。
在批改前，请先自动判断作文语言类型：
- 如果是中文作文，则按照语文作文标准进行评价。
- 如果是英文作文，则按照英语写作标准进行评价。

作文要求：
{essay_requirements}

学生作文原文：
{essay_text}

请严格返回纯 JSON，不要添加 Markdown 或解释文字。JSON 字段如下：
{{
  "score": 85,
  "language_type": "中文作文 或 英文作文",
  "advantages": "优点。中文作文按立意、结构、语言表达、描写、情感等方面总结；英文作文按词汇使用、句式多样性、内容完整性、逻辑性等方面总结。必须具体，避免空泛。",
  "disadvantages": "不足或缺点分析。中文作文指出逻辑不清、内容空泛、结构松散、错别字、表达问题等；英文作文分清拼写/单词错误与其他问题，单词/拼写错误必须集中归类列出正确拼写与错误情况，其他问题再分析语法、时态、句子结构、搭配等。",
  "suggestions": [
    {{
      "original_sentence": "引用原文中需要改进的句子或问题点",
      "revised_sentence": "给出更自然、更高级或更准确的改写",
      "reason": "解释修改原因"
    }}
  ],
  "summary_comment": "综合提升建议。中文作文给出具体可执行的修改方向；英文作文给出整体英语写作提升建议，如句式复杂化、连接词使用、中式英语避免等。"
}}

中文作文批改要求：
1. 按“优点—不足—修改建议”的结构组织内容。
2. 优点要覆盖立意、结构、语言表达、描写或情感等可观察方面。
3. 不足要指出主要问题，例如逻辑不清、内容空泛、结构松散、错别字或表达问题。
4. 修改建议必须具体可执行，尽量结合原文进行优化说明，不要只指出问题。

英文作文批改要求：
1. 按“优点—缺点分析—句式升级建议—综合提升建议”的结构组织内容。
2. 单词/拼写错误必须统一归类列出，集中说明错误拼写、正确拼写与错误情况，不要分散讲解。
3. 其他问题包括语法错误、时态问题、句子结构问题和搭配问题等，需单独分析。
4. suggestions 必须提供至少 5 条句式升级或改写建议；如果作文质量较差，增加到 8 至 10 条。
5. 每条 suggestions 必须包含原句或问题表达、修改后的更优表达、简短原因说明。
6. summary_comment 必须给出整体英语写作提升建议，如句式复杂化、连接词使用、中式英语避免等。

整体要求：
1. 评价必须具体、可操作，避免空泛评价。
2. 不要只指出问题，必须提供明确修改方法。
3. 如果图片内容不是作文，也要返回上述 JSON，score 给 0，并在 disadvantages 和 summary_comment 中说明原因。
"""


NAME_EXTRACTION_PROMPT_TEMPLATE = """
从下面的作文文本中提取学生姓名。姓名通常在开头、结尾、姓名/班级标签旁，或单独成行。
只返回姓名本身，不要解释；如果无法判断，返回“未知学生”。

文本：
---
{essay_text}
"""


OVERALL_ANALYSIS_PROMPT_TEMPLATE = """
你是一名英语教研组长。请根据本次批量批阅结果，分析全班/本批学生总体写作情况。

本批结果 JSON：
{batch_json}

请严格返回纯 JSON，不要添加 Markdown 或解释文字。字段如下：
{{
  "overview": "一句话概括本批作文整体水平。",
  "score_distribution": "概括分数分布、平均分、最高/最低区间。",
  "common_strengths": ["共性优点1", "共性优点2"],
  "common_issues": ["共性问题1", "共性问题2"],
  "teaching_focus": ["下一节课建议重点1", "下一节课建议重点2"],
  "student_groups": [
    {{
      "group": "需要重点关注",
      "students": ["学生A"],
      "reason": "分数较低或问题集中"
    }}
  ]
}}
"""


class LLMService:
    def __init__(self):
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        self.temperature = 0.2
        self.max_tokens = 4096

    def _runtime_config(self) -> Dict[str, str]:
        config = teacher_config_service.get_llm_config()
        if not config.get("api_key"):
            raise ValueError("尚未配置火山方舟 API Key，请先到“AI配置”页面填写。")
        return config

    def _headers(self, api_key: str) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _detect_mime(image_bytes: bytes) -> str:
        if image_bytes.startswith(b"\x89PNG"):
            return "image/png"
        if image_bytes.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if image_bytes.startswith(b"BM"):
            return "image/bmp"
        return "image/jpeg"

    def _image_data_url(self, image_bytes: bytes) -> str:
        mime = self._detect_mime(image_bytes)
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:{mime};base64,{encoded}"

    def _extract_json_from_response(self, response: str) -> str:
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        json_str = json_match.group(0) if json_match else response.strip()
        return re.sub(r",(\s*[}\]])", r"\1", json_str)

    def _normalize_grading_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if "advantages" not in result and "strengths" in result:
            result["advantages"] = result.pop("strengths")
        if "disadvantages" not in result and "weaknesses" in result:
            result["disadvantages"] = result.pop("weaknesses")

        required = ["score", "advantages", "disadvantages", "suggestions", "summary_comment"]
        missing = [field for field in required if field not in result]
        if missing:
            raise ValueError(f"批阅结果缺少必要字段: {', '.join(missing)}")

        score = float(result["score"])
        if not 0 <= score <= 100:
            raise ValueError(f"分数超出范围: {score}")
        result["score"] = score

        if not isinstance(result["suggestions"], list):
            raise ValueError("suggestions 字段必须是列表")
        return result

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8), reraise=True)
    async def _call_messages(self, messages: List[Dict[str, Any]], *, temperature: float | None = None) -> str:
        config = self._runtime_config()
        payload = {
            "model": config["model_id"],
            "messages": messages,
            "temperature": self.temperature if temperature is None else temperature,
            "max_tokens": self.max_tokens,
        }

        logger.info("正在调用豆包模型: %s", config["model_id"])
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                self.api_url,
                headers=self._headers(config["api_key"]),
                json=payload,
            )
            response.raise_for_status()

        response_data = response.json()
        content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            raise ValueError("LLM API 返回内容为空")
        return content

    async def recognize_image_text(self, image_bytes: bytes, purpose: str) -> str:
        if not image_bytes:
            raise ValueError("输入的图片数据不能为空")

        prompt = (
            f"请识别这张图片中的{purpose}。"
            "要求尽量保留原文、换行、学生姓名、班级和题目要求。"
            "只返回识别出的文本，不要添加解释。"
        )
        messages = [
            {"role": "system", "content": "你是一个高准确率的图片文字识别助手。"},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": self._image_data_url(image_bytes)}},
                ],
            },
        ]
        text = await self._call_messages(messages, temperature=0.0)
        return text.strip()

    async def extract_student_name(self, essay_text: str) -> str:
        prompt = NAME_EXTRACTION_PROMPT_TEMPLATE.format(essay_text=essay_text)
        name = await self._call_messages(
            [
                {"role": "system", "content": "你负责从文本中提取学生姓名，只返回姓名。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        cleaned_name = name.strip().replace("姓名：", "").replace("姓名:", "").strip()
        return cleaned_name or "未知学生"

    async def grade_essay(self, requirements: str, essay_text: str) -> Dict[str, Any]:
        prompt = GRADING_PROMPT_TEMPLATE.format(
            essay_requirements=requirements,
            essay_text=essay_text,
        )
        response_text = await self._call_messages(
            [
                {"role": "system", "content": "你是专业的中英文作文批改老师，必须严格返回 JSON。"},
                {"role": "user", "content": prompt},
            ]
        )

        try:
            result = json.loads(self._extract_json_from_response(response_text))
            return self._normalize_grading_result(result)
        except Exception as exc:
            logger.error("LLM 原始批阅响应: %s", response_text)
            raise ValueError(f"LLM 返回的批阅结果格式不正确: {exc}") from exc

    async def analyze_batch(self, summary: Dict[str, Any], details: List[Dict[str, Any]]) -> Dict[str, Any]:
        compact_details = []
        for item in details:
            grading = item.get("grading_result") or {}
            compact_details.append({
                "student_name": item.get("student_name"),
                "saved_to_db": item.get("saved_to_db"),
                "error": item.get("error"),
                "score": grading.get("score"),
                "advantages": grading.get("advantages"),
                "disadvantages": grading.get("disadvantages"),
                "summary_comment": grading.get("summary_comment"),
            })

        prompt = OVERALL_ANALYSIS_PROMPT_TEMPLATE.format(
            batch_json=json.dumps(
                {"summary": summary, "details": compact_details},
                ensure_ascii=False,
            )
        )
        response_text = await self._call_messages(
            [
                {"role": "system", "content": "你是英语教研组长，严格返回 JSON。"},
                {"role": "user", "content": prompt},
            ]
        )

        try:
            return json.loads(self._extract_json_from_response(response_text))
        except Exception as exc:
            logger.error("LLM 原始总体分析响应: %s", response_text)
            return {
                "overview": "总体分析生成失败，请查看单个学生批阅结果。",
                "common_strengths": [],
                "common_issues": [str(exc)],
                "teaching_focus": [],
                "student_groups": [],
            }
