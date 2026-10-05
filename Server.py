#If you need to run it on a personal computer
#Please enter the following cmd command
#cd CatVaultServer-side
#python -m uvicorn Server:app --reload

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from Supports import Check
from Supports import VaultError

app = FastAPI()
STORAGE = Path("storage")
STORAGE.mkdir(exist_ok=True)


@app.post("/{username}/backup/{filename}/")
async def backup(username: str, filename: str, file: UploadFile = File(...)):
    Check.Check(name=[[username, filename], ['/', '\\', '..']]).check_name()

    user_dir = STORAGE / username              # 目录
    user_dir.mkdir(parents=True, exist_ok=True)

    save_path = user_dir / filename            # 文件
    with save_path.open("wb") as f:
        f.write(await file.read())
    return {"ok": True, "path": str(save_path.absolute())}


@app.get("/{username}/backup/{filename}/")
def restore(username: str, filename: str):
    Check.Check(name=[[username, filename], ['/', '\\', '..']]).check_name()

    path = STORAGE / username / filename
    if not path.exists():
        raise VaultError.VaultError.FileNotFound(f"找不到文件: {filename}")
    return FileResponse(path, filename=filename)


@app.delete("/{username}/files/{filename}/")
def delete_file(username: str, filename: str):
    Check.Check(name=[[username, filename], ['/', '\\', '..']]).check_name()

    path = STORAGE / username / filename
    if not path.exists():
        raise VaultError.VaultError.FileNotFound(f"找不到文件: {filename}")
    path.unlink()
    return {"ok": True}


@app.exception_handler(VaultError.VaultError)
async def vault_error_handler(request: Request, exc: VaultError.VaultError):
    if isinstance(exc, VaultError.FileNotFound):
        status = 404
    elif isinstance(exc, VaultError.InvalidName):
        status = 400
    elif isinstance(exc, VaultError.AuthFailed):
        status = 401
    elif isinstance(exc, VaultError.FileTooLarge):
        status = 413
    else:
        status = 500

    return JSONResponse(
        status_code=status,
        content={
            "ok": False,
            "error": type(exc).__name__,
            "message": exc.message,
        }
    )