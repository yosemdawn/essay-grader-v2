"""
Windows packaged launcher.

Double-clicking the packaged exe starts the FastAPI server and opens the browser.
"""
import threading
import time
import webbrowser

import uvicorn

from app.config import settings
from main import app


def open_browser_later() -> None:
    time.sleep(2)
    webbrowser.open(f"http://127.0.0.1:{settings.port}")


if __name__ == "__main__":
    threading.Thread(target=open_browser_later, daemon=True).start()
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level="info",
    )
