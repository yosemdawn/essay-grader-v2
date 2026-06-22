import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape
from typing import Any, Dict

from app.services.teacher_config import teacher_config_service


logger = logging.getLogger(__name__)


def _format_value(value: Any) -> str:
    if value is None or value == "":
        return "暂无"
    if isinstance(value, list):
        return "<br>".join(f"{idx}. {escape(str(item))}" for idx, item in enumerate(value, 1))
    if isinstance(value, dict):
        return "<br>".join(
            f"<strong>{escape(str(key))}：</strong>{escape(str(val))}"
            for key, val in value.items()
        )
    return escape(str(value)).replace("\n", "<br>")


class EmailService:
    """Send grading reports through the teacher-configured SMTP account."""

    def __init__(self):
        config = teacher_config_service.get_email_config()
        self.enabled = bool(config.get("enabled"))
        self.smtp_host = config.get("smtp_host") or "smtp.qq.com"
        self.smtp_port = int(config.get("smtp_port") or 465)
        self.smtp_username = config.get("smtp_username") or ""
        self.smtp_password = config.get("smtp_password") or ""

    def is_configured(self) -> bool:
        return bool(self.enabled and self.smtp_host and self.smtp_username and self.smtp_password)

    def _render_email_template(self, student_name: str, grading_result: Dict) -> str:
        score = grading_result.get("score", "N/A")
        advantages = grading_result.get("advantages", grading_result.get("strengths"))
        disadvantages = grading_result.get("disadvantages", grading_result.get("weaknesses"))
        suggestions = grading_result.get("suggestions")
        summary = grading_result.get("summary_comment") or grading_result.get("summary") or ""
        sentence_upgrades = grading_result.get("sentence_upgrades")
        spelling_errors = grading_result.get("spelling_errors")

        extra_sections = ""
        if spelling_errors:
            extra_sections += f"""
            <div class="section">
              <h3>单词/拼写错误汇总</h3>
              <p>{_format_value(spelling_errors)}</p>
            </div>
            """
        if sentence_upgrades:
            extra_sections += f"""
            <div class="section">
              <h3>句式升级建议</h3>
              <p>{_format_value(sentence_upgrades)}</p>
            </div>
            """

        return f"""
        <!doctype html>
        <html lang="zh-CN">
        <head>
          <meta charset="utf-8">
          <style>
            body {{
              margin: 0;
              padding: 24px;
              background: #f4f6f8;
              color: #1f2933;
              font-family: "Microsoft YaHei", Arial, sans-serif;
              line-height: 1.75;
            }}
            .container {{
              max-width: 760px;
              margin: 0 auto;
              background: #ffffff;
              border: 1px solid #e5e7eb;
              border-radius: 10px;
              overflow: hidden;
            }}
            .header {{
              padding: 24px 28px;
              background: #1f4e79;
              color: #ffffff;
            }}
            .header h2 {{ margin: 0; font-size: 22px; }}
            .content {{ padding: 24px 28px; }}
            .score {{
              display: inline-block;
              min-width: 88px;
              padding: 10px 16px;
              margin: 8px 0 18px;
              border-radius: 8px;
              background: #eef6ff;
              color: #1f4e79;
              font-size: 28px;
              font-weight: 700;
              text-align: center;
            }}
            .section {{
              margin: 0 0 18px;
              padding: 16px;
              border: 1px solid #e5e7eb;
              border-radius: 8px;
              background: #fbfcfd;
            }}
            .section h3 {{
              margin: 0 0 8px;
              color: #1f4e79;
              font-size: 16px;
            }}
            .section p {{ margin: 0; }}
            .footer {{
              padding: 14px 28px 22px;
              color: #6b7280;
              font-size: 13px;
            }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h2>{escape(student_name)} 同学的作文批阅报告</h2>
            </div>
            <div class="content">
              <div>综合得分</div>
              <div class="score">{escape(str(score))}</div>

              <div class="section">
                <h3>优点</h3>
                <p>{_format_value(advantages)}</p>
              </div>

              <div class="section">
                <h3>不足/问题分析</h3>
                <p>{_format_value(disadvantages)}</p>
              </div>

              <div class="section">
                <h3>修改建议</h3>
                <p>{_format_value(suggestions)}</p>
              </div>

              {extra_sections}

              <div class="section">
                <h3>综合评语</h3>
                <p>{_format_value(summary)}</p>
              </div>
            </div>
            <div class="footer">
              本邮件由 AI 作文批阅系统自动发送。请结合课堂要求继续修改完善。
            </div>
          </div>
        </body>
        </html>
        """

    async def send_grading_email(
        self,
        student_name: str,
        student_email: str,
        grading_result: Dict,
    ) -> bool:
        if not student_email:
            logger.info("Skip email: student email is empty for %s", student_name)
            return False
        if not self.is_configured():
            logger.info("Skip email: SMTP is not enabled or incomplete.")
            return False

        subject = f"【作文批阅报告】{student_name}同学，你的作文已批阅"
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.smtp_username
        msg["To"] = student_email
        msg.attach(MIMEText(self._render_email_template(student_name, grading_result), "html", "utf-8"))

        try:
            if self.smtp_port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context, timeout=30) as server:
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            logger.info("Email sent to %s <%s>", student_name, student_email)
            return True
        except Exception as exc:
            logger.error("Failed to send email to %s <%s>: %s", student_name, student_email, exc, exc_info=True)
            return False
