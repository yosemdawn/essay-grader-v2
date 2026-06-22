"""
Teacher-managed runtime configuration.

The API key is intentionally stored outside source code in data/teacher_config.json.
"""
import json
from pathlib import Path
from typing import Any, Dict

from app.config import settings
from app.paths import TEACHER_CONFIG_PATH


DEFAULT_MODEL_ID = "doubao-seed-2-0-lite-260428"


class TeacherConfigService:
    def __init__(self, config_path: Path = TEACHER_CONFIG_PATH):
        self.config_path = config_path

    def _read_raw(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return {}
        try:
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _write_raw(self, data: Dict[str, Any]) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get_llm_config(self) -> Dict[str, str]:
        data = self._read_raw()
        return {
            "model_id": data.get("model_id") or settings.doubao_model_id or DEFAULT_MODEL_ID,
            "api_key": data.get("api_key") or settings.doubao_api_key or "",
        }

    def get_email_config(self) -> Dict[str, Any]:
        data = self._read_raw()
        email = data.get("email") or {}
        return {
            "enabled": bool(email.get("enabled", False)),
            "smtp_host": email.get("smtp_host") or settings.smtp_host or "smtp.qq.com",
            "smtp_port": int(email.get("smtp_port") or settings.smtp_port or 465),
            "smtp_username": email.get("smtp_username") or settings.smtp_username or "",
            "smtp_password": email.get("smtp_password") or settings.smtp_password or "",
        }

    def update_llm_config(self, model_id: str, api_key: str) -> Dict[str, str]:
        model_id = (model_id or DEFAULT_MODEL_ID).strip()
        api_key = (api_key or "").strip()
        data = self._read_raw()
        data.update({"model_id": model_id, "api_key": api_key})
        self._write_raw(data)
        return self.get_public_llm_config()

    def update_email_config(
        self,
        enabled: bool,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str = "",
    ) -> Dict[str, Any]:
        data = self._read_raw()
        current = data.get("email") or {}
        password = (smtp_password or "").strip() or current.get("smtp_password") or ""
        data["email"] = {
            "enabled": bool(enabled),
            "smtp_host": (smtp_host or "smtp.qq.com").strip(),
            "smtp_port": int(smtp_port or 465),
            "smtp_username": (smtp_username or "").strip(),
            "smtp_password": password,
        }
        self._write_raw(data)
        return self.get_public_email_config()

    def get_public_llm_config(self) -> Dict[str, Any]:
        config = self.get_llm_config()
        api_key = config["api_key"]
        return {
            "model_id": config["model_id"],
            "api_key_configured": bool(api_key),
            "api_key_masked": self.mask_key(api_key),
        }

    def get_public_email_config(self) -> Dict[str, Any]:
        config = self.get_email_config()
        password = config["smtp_password"]
        return {
            "enabled": config["enabled"],
            "smtp_host": config["smtp_host"],
            "smtp_port": config["smtp_port"],
            "smtp_username": config["smtp_username"],
            "smtp_password_configured": bool(password),
            "smtp_password_masked": self.mask_key(password),
        }

    @staticmethod
    def mask_key(api_key: str) -> str:
        if not api_key:
            return ""
        if len(api_key) <= 8:
            return "*" * len(api_key)
        return f"{api_key[:4]}***{api_key[-4:]}"


teacher_config_service = TeacherConfigService()
