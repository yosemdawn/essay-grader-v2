"""
Teacher-facing runtime settings APIs.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.models.database import User
from app.services.teacher_config import DEFAULT_MODEL_ID, teacher_config_service
from app.utils.dependencies import require_admin


router = APIRouter(
    prefix="/api/settings",
    tags=["settings"],
    dependencies=[Depends(require_admin)],
)


class LLMConfigResponse(BaseModel):
    model_id: str
    api_key_configured: bool
    api_key_masked: str = ""


class LLMConfigUpdateRequest(BaseModel):
    model_id: str = Field(default=DEFAULT_MODEL_ID, min_length=1)
    api_key: str = Field(min_length=1)


class EmailConfigResponse(BaseModel):
    enabled: bool
    smtp_host: str
    smtp_port: int
    smtp_username: str = ""
    smtp_password_configured: bool
    smtp_password_masked: str = ""


class EmailConfigUpdateRequest(BaseModel):
    enabled: bool = True
    smtp_host: str = Field(default="smtp.qq.com", min_length=1)
    smtp_port: int = Field(default=465, ge=1, le=65535)
    smtp_username: str = ""
    smtp_password: str = ""


@router.get("/llm", response_model=LLMConfigResponse, summary="Read AI model config")
async def get_llm_config(current_user: User = Depends(require_admin)):
    return teacher_config_service.get_public_llm_config()


@router.put("/llm", response_model=LLMConfigResponse, summary="Save AI model config")
async def update_llm_config(
    request: LLMConfigUpdateRequest,
    current_user: User = Depends(require_admin),
):
    try:
        return teacher_config_service.update_llm_config(
            model_id=request.model_id,
            api_key=request.api_key,
        )
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存 AI 配置失败: {exc}",
        ) from exc


@router.get("/email", response_model=EmailConfigResponse, summary="Read email config")
async def get_email_config(current_user: User = Depends(require_admin)):
    return teacher_config_service.get_public_email_config()


@router.put("/email", response_model=EmailConfigResponse, summary="Save email config")
async def update_email_config(
    request: EmailConfigUpdateRequest,
    current_user: User = Depends(require_admin),
):
    try:
        return teacher_config_service.update_email_config(
            enabled=request.enabled,
            smtp_host=request.smtp_host,
            smtp_port=request.smtp_port,
            smtp_username=request.smtp_username,
            smtp_password=request.smtp_password,
        )
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存邮件配置失败: {exc}",
        ) from exc
