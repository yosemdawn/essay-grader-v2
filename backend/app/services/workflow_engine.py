import logging
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from .email_service import EmailService
from .grading_db import grading_db_service
from .llm_service import LLMService


logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Coordinates the essay grading flow.

    Images are recognized by the configured Doubao model instead of a separate OCR API.
    """

    def __init__(self, db: Optional[Session] = None):
        self.llm_service = LLMService()
        self.grading_db = grading_db_service
        self.db = db

    async def process_single_essay(
        self,
        essay_image_bytes: bytes,
        requirements: str,
        image_path: Optional[str] = None,
    ) -> Dict:
        result = {
            "student_name": "未知学生",
            "student_id": None,
            "grading_result": None,
            "saved_to_db": False,
            "email_sent": False,
            "email_error": None,
            "error": None,
        }

        try:
            logger.info("Step 1/5: recognizing essay image with AI...")
            essay_text = await self.llm_service.recognize_image_text(
                essay_image_bytes,
                "学生作文全文",
            )
            if not essay_text.strip():
                raise ValueError("AI 未能识别出任何作文文本")

            logger.info("Step 2/5: extracting student name...")
            student_name = await self.llm_service.extract_student_name(essay_text)
            result["student_name"] = student_name

            logger.info("Step 3/5: grading essay for %s...", student_name)
            grading_result = await self.llm_service.grade_essay(requirements, essay_text)
            result["grading_result"] = grading_result

            logger.info("Step 4/5: saving grading result...")
            save_result = self.grading_db.save_grading_result(
                student_name=student_name,
                essay_text=essay_text,
                requirements=requirements,
                grading_result=grading_result,
                image_path=image_path,
                db=self.db,
            )

            if not save_result["success"]:
                result["error"] = save_result.get("error")
                logger.error("Failed to save grading result: %s", save_result.get("error"))
                return result

            result["saved_to_db"] = True
            result["student_id"] = save_result.get("student_id")
            result["essay_id"] = save_result.get("essay_id")
            result["grading_record_id"] = save_result.get("grading_record_id")
            logger.info(
                "Saved grading result for %s (Record ID: %s)",
                student_name,
                save_result.get("grading_record_id"),
            )

            logger.info("Step 5/5: sending grading email if configured...")
            student_email = save_result.get("student_email")
            if not student_email:
                result["email_error"] = "学生未填写邮箱，已跳过邮件发送。"
                return result

            email_service = EmailService()
            result["email_sent"] = await email_service.send_grading_email(
                student_name=student_name,
                student_email=student_email,
                grading_result=grading_result,
            )
            if not result["email_sent"] and email_service.is_configured():
                result["email_error"] = "邮件发送失败，请检查 QQ 邮箱授权码或网络。"

        except Exception as e:
            logger.error("Failed to process essay: %s", e, exc_info=True)
            result["error"] = str(e)

        return result

    async def process_batch(
        self,
        prompt_image_bytes: bytes,
        essay_images_bytes: List[bytes],
        progress_callback=None,
    ) -> Dict:
        total_count = len(essay_images_bytes)
        logger.info("Start batch grading, total essays: %s", total_count)

        if progress_callback:
            progress_callback(0, "AI 识别作文要求...")

        try:
            requirements = await self.llm_service.recognize_image_text(
                prompt_image_bytes,
                "作文题目和写作要求",
            )
            if not requirements.strip():
                raise ValueError("AI 未能识别出任何作文要求")
        except Exception as e:
            logger.error("Failed to recognize essay requirements: %s", e)
            return {
                "error": f"无法处理作文要求图片: {e}",
                "summary": {
                    "total_essays": total_count,
                    "successful_grades": 0,
                    "failed_grades": total_count,
                    "saved_to_db": 0,
                    "email_sent": 0,
                    "average_score": 0,
                },
                "details": [],
                "overall_analysis": None,
            }

        results = []
        completed_count = 0

        for index, essay_bytes in enumerate(essay_images_bytes):
            if progress_callback:
                progress_callback(completed_count, f"处理第 {index + 1}/{total_count} 篇作文...")

            result = await self.process_single_essay(essay_bytes, requirements)
            results.append(result)
            completed_count += 1

            if progress_callback:
                progress_callback(completed_count, f"已完成 {completed_count}/{total_count} 篇作文")

        if progress_callback:
            progress_callback(completed_count, "分析学生总体写作情况...")

        final_report = self.generate_final_report(results)
        try:
            final_report["overall_analysis"] = await self.llm_service.analyze_batch(
                final_report["summary"],
                results,
            )
        except Exception as e:
            logger.error("Failed to generate overall analysis: %s", e)
            final_report["overall_analysis"] = {
                "overview": "总体分析生成失败，请查看单个学生批阅结果。",
                "score_distribution": "",
                "common_strengths": [],
                "common_issues": [str(e)],
                "teaching_focus": [],
                "student_groups": [],
            }

        logger.info("Batch grading complete.")
        return final_report

    def generate_final_report(self, results: List[Dict]) -> Dict:
        total_essays = len(results)
        successful_grades = sum(1 for r in results if r.get("grading_result") and not r.get("error"))
        failed_grades = total_essays - successful_grades
        saved_to_db = sum(1 for r in results if r.get("saved_to_db", False))
        email_sent = sum(1 for r in results if r.get("email_sent", False))

        total_score = 0.0
        scored_essays = 0
        for result in results:
            grading = result.get("grading_result") or {}
            if grading.get("score") is not None:
                try:
                    total_score += float(grading["score"])
                    scored_essays += 1
                except (ValueError, TypeError):
                    continue

        average_score = round(total_score / scored_essays, 2) if scored_essays else 0

        return {
            "summary": {
                "total_essays": total_essays,
                "successful_grades": successful_grades,
                "failed_grades": failed_grades,
                "saved_to_db": saved_to_db,
                "email_sent": email_sent,
                "average_score": average_score,
            },
            "details": results,
        }
