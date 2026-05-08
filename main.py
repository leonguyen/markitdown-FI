from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from markitdown import MarkItDownOptions, MarkItDown
import tempfile
import os

app = FastAPI(
    title="MarkItDown API",
    description="HTTP wrapper around Microsoft MarkItDown for document → Markdown conversion.",
    version="0.1.4"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/convert")
async def convert(
    file: UploadFile = File(...),
    max_pages: int = 10,
    markdown_flavor: str = "commonmark",
):
    """Convert uploaded file to Markdown."""

    # Guard on file size (e.g. 100 MB)
    if file.content_type in ["text/plain", "text/markdown"]:
        max_bytes = 10 * 1024 * 1024  # 10 MB
    else:
        max_bytes = 100 * 1024 * 1024  # 100 MB

    contents = await file.read()
    if len(contents) > max_bytes:
        raise HTTPException(status_code=400, detail="File too large")

    # Write to temp file
    with tempfile.NamedTemporaryFile(
        suffix=os.path.splitext(file.filename)[1],
        delete=False
    ) as f:
        f.write(contents)
        temp_path = f.name

    try:
        opts = MarkItDownOptions(
            max_pages=max_pages,
            markdown_flavor=markdown_flavor,
        )
        m = MarkItDown(opts)
        result = m.convert(temp_path)

        return JSONResponse({
            "filename": file.filename,
            "markdown": result.document,
            "diagnostics": result.diagnostics,
        })
    finally:
        os.unlink(temp_path)
