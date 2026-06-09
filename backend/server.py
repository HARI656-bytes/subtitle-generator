import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional
from datetime import timedelta
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, BackgroundTasks
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(title="Video Subtitle Generator API")

def extract_audio(video_path: Path, output_audio_path: Path) -> None:
    try:
        import ffmpeg
        stream = ffmpeg.input(str(video_path))
        stream = ffmpeg.output(stream['a'], str(output_audio_path), acodec='pcm_s16le', ar='16000')
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True)
        if not output_audio_path.exists():
            raise RuntimeError("Audio file was not created")
    except Exception as e:
        raise RuntimeError(f"Failed to extract audio: {str(e)}")

def transcribe_audio(audio_path: Path, language: Optional[str] = None) -> dict:
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(str(audio_path), language=language, verbose=False)
        return result
    except Exception as e:
        raise RuntimeError(f"Failed to transcribe audio: {str(e)}")

def format_timestamp(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(int(td.total_seconds()), 3600)
    minutes, seconds_int = divmod(remainder, 60)
    milliseconds = int((td.total_seconds() % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"

def generate_srt_subtitle(transcription: dict) -> str:
    srt_content = []
    for index, segment in enumerate(transcription['segments'], 1):
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        text = segment['text'].strip()
        if not text:
            continue
        srt_entry = f"{index}\n{start_time} --> {end_time}\n{text}\n"
        srt_content.append(srt_entry)
    return "\n".join(srt_content)

@app.post("/generate-subtitles/")
async def generate_subtitles(file: UploadFile = File(...), language: Optional[str] = Form(None)):
    supported_formats = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm'}
    ext = Path(file.filename).suffix.lower()
    if ext not in supported_formats:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {ext}")

    temp_dir = tempfile.mkdtemp()
    temp_dir_path = Path(temp_dir)
    video_path = temp_dir_path / file.filename
    audio_path = temp_dir_path / "audio.wav"
    srt_path = temp_dir_path / f"{Path(file.filename).stem}.srt"

    try:
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extract_audio(video_path, audio_path)
        transcription = transcribe_audio(audio_path, language if language else None)
        srt_content = generate_srt_subtitle(transcription)

        if not srt_content.strip():
            raise RuntimeError("No subtitles were generated from the video")

        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)

        def cleanup_temp_dir():
            shutil.rmtree(temp_dir_path, ignore_errors=True)

        from starlette.background import BackgroundTask
        return FileResponse(
            path=srt_path, 
            media_type='text/plain', 
            filename=srt_path.name,
            background=BackgroundTask(cleanup_temp_dir)
        )
    except Exception as e:
        shutil.rmtree(temp_dir_path, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
