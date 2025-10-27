import asyncio
import os
import pty
import shlex
import signal
import subprocess
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


ROOT = Path(__file__).parent
WEB_DIR = ROOT / "web"

app = FastAPI()


# Serve the static frontend
if WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(WEB_DIR), html=True), name="web")


async def _read_pty_to_ws(fd: int, ws: WebSocket):
    loop = asyncio.get_running_loop()
    try:
        while True:
            data: bytes = await loop.run_in_executor(None, os.read, fd, 4096)
            if not data:
                break
            try:
                # Send as text so the browser terminal receives string frames
                await ws.send_text(data.decode(errors="ignore"))
            except Exception as e:
                print(f"Error sending to websocket: {e}")
                break
    except Exception as e:
        print(f"Error reading from PTY: {e}")
        pass


@app.websocket("/ws")
async def ws_terminal(websocket: WebSocket):
    await websocket.accept()

    # Spawn the game in a pseudo-terminal so ANSI and input behave well
    master_fd, slave_fd = pty.openpty()

    env = os.environ.copy()
    # Make sure we run with unbuffered output
    env["PYTHONUNBUFFERED"] = "1"

    cmd = ["python3", str(ROOT / "game.py")]

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            env=env,
            cwd=str(ROOT),
            close_fds=False,
        )
    finally:
        # We don't need the slave in this process
        os.close(slave_fd)

    reader_task = asyncio.create_task(_read_pty_to_ws(master_fd, websocket))

    try:
        while True:
            try:
                msg = await websocket.receive_text()
            except WebSocketDisconnect:
                break
            except Exception:
                break
            # Ensure a trailing newline to simulate Enter
            data = (msg if msg.endswith("\n") else msg + "\n").encode()
            try:
                os.write(master_fd, data)
            except Exception:
                break
    finally:
        try:
            reader_task.cancel()
        except Exception:
            pass
        try:
            os.close(master_fd)
        except Exception:
            pass
        try:
            # Terminate subprocess
            proc.terminate()
        except Exception:
            pass
        try:
            proc.wait(timeout=2)
        except Exception:
            pass


@app.get("/")
async def root():
    with open(WEB_DIR / "index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
async def health():
    return {"ok": True}


def main() -> None:
    import uvicorn

    # Render sets PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()


