"""
牛逼格拉斯yosem - AI作文批阅系统
主应用入口文件
"""
import logging
import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.routes.grading import router as grading_router
from app.routes.students import router as students_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.records import router as records_router
from app.routes.settings import router as settings_router
from app.tasks.task_manager import task_manager
from app.paths import ensure_directories, APP_LOG, STATIC_DIR, TEMPLATES_DIR, FRONTEND_DIST_DIR
from app.database import init_db

# 确保目录存在
ensure_directories()

# 配置日志
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(APP_LOG, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 牛逼格拉斯yosem AI作文批阅系统启动中...")
    
    # 确保必要的目录存在（已在导入时执行）
    logger.info("📁 目录结构检查完成")
    
    # 初始化数据库
    try:
        init_db()
        logger.info("💾 数据库初始化完成")
    except Exception as e:
        logger.warning(f"数据库初始化警告: {e}")
    
    # 启动任务管理器
    task_manager.start()
    logger.info("⚙️  后台任务管理器已启动")
    
    logger.info("✅ 系统初始化完成")
    yield
    
    # 关闭时执行
    logger.info("👋 系统正在关闭...")


# 创建FastAPI应用
app = FastAPI(
    title="牛逼格拉斯yosem - AI作文批阅系统",
    description="""
    🤖 智能AI作文批阅系统
    
    ## 主要功能
    
    * **📝 作文批阅**: 支持单篇和批量作文批阅
    * **🔍 OCR识别**: 智能图片文字识别
    * **🤖 AI评分**: 专业的作文评分和建议
    * **📧 邮件通知**: 自动发送批阅结果
    * **👥 学生管理**: 完整的学生信息管理系统
    * **📊 数据统计**: 批阅数据统计和分析
    
    ## API文档
    
    * 作文批阅接口: `/api/grading/`
    * 学生管理接口: `/api/students/`
    
    ## 技术特色
    
    * 🚀 FastAPI + 异步处理
    * 🔍 百度OCR + 豆包LLM
    * 📧 智能邮件发送
    * 🎯 工作流引擎
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 模板引擎
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 注册路由
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(records_router)
app.include_router(grading_router)
app.include_router(students_router)
app.include_router(settings_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error_code": exc.status_code
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证异常处理器"""
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "请求参数验证失败",
            "errors": exc.errors(),
            "error_code": 422
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "服务器内部错误",
            "error_code": 500
        }
    )

 
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """主页"""
    frontend_index = FRONTEND_DIST_DIR / "index.html"
    if frontend_index.exists():
        return FileResponse(frontend_index)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "牛逼格拉斯yosem AI作文批阅系统",
        "version": "1.0.0"
    }


@app.get("/api/info")
async def api_info():
    """API信息"""
    return {
        "service": "牛逼格拉斯yosem AI作文批阅系统",
        "version": "1.0.0",
        "description": "智能AI作文批阅系统",
        "features": [
            "OCR文字识别",
            "AI智能批阅",
            "邮件自动发送",
            "学生信息管理",
            "批量处理支持",
            "实时进度跟踪"
        ],
        "endpoints": {
            "grading": "/api/grading/",
            "students": "/api/students/",
            "docs": "/docs",
            "health": "/health"
        }
    }


if FRONTEND_DIST_DIR.exists():
    assets_dir = FRONTEND_DIST_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="frontend-assets")


@app.get("/{full_path:path}", response_class=HTMLResponse)
async def frontend_spa_fallback(full_path: str, request: Request):
    """Serve the Vue app for non-API routes in packaged/local production mode."""
    if full_path.startswith(("api/", "docs", "redoc", "openapi.json", "static/")):
        raise HTTPException(status_code=404, detail="Not found")

    frontend_index = FRONTEND_DIST_DIR / "index.html"
    if frontend_index.exists():
        candidate = (FRONTEND_DIST_DIR / full_path).resolve()
        try:
            candidate.relative_to(FRONTEND_DIST_DIR.resolve())
        except ValueError:
            candidate = None

        if candidate and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(frontend_index)

    raise HTTPException(status_code=404, detail="Frontend build not found")


if __name__ == "__main__":
    # 运行应用
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
