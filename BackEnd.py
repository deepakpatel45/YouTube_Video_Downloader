from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import yt_dlp

app = FastAPI()

# Setup template rendering (for HTML)
templates = Jinja2Templates(directory="templates")


def download_youtube_video(url, output_path="."):
    options = {
        'format': 'best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
            return "Download completed!"
    except Exception as e:
        return f"An error occurred: {e}"


# Render the HTML page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Handle form submission
@app.post("/download/")
async def download_video(url: str = Form(...)):
    result = download_youtube_video(url)
    return {"message": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
