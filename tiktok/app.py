from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os

app = FastAPI()

# Define download folder
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TikTok Video Downloader</title>
    </head>
    <body>
        <h1>Enter TikTok Video URL</h1>
        <form action="/download/" method="post">
            <input type="text" name="url" required>
            <input type="submit" value="Download">
        </form>
    </body>
    </html>
    """

def download_tiktok_video(url: str):
    """ Downloads a TikTok video using yt_dlp and returns the file path. """
    video_path = os.path.join(DOWNLOAD_FOLDER, "tiktok_video.mp4")

    ydl_opts = {
        'outtmpl': video_path,  # Save the file in the download folder
        'quiet': True,  # Suppress console output
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return video_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/download/")
async def download_video(url: str = Form(...)):
    """ API endpoint to handle video download and return the file. """
    video_path = download_tiktok_video(url)

    if not os.path.exists(video_path):
        raise HTTPException(status_code=500, detail="Failed to download video.")

    # Send the file to the user (opens a "Save File" dialog in browser)
    return FileResponse(video_path, media_type='video/mp4', filename="tiktok_video.mp4")
