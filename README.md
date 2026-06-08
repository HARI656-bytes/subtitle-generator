# Video Subtitle Generator

## Overview

Video Subtitle Generator is a desktop application built using Flet and FastAPI that automatically generates subtitle (.srt) files from video files using OpenAI Whisper.

### Features

* Upload MP4, MKV, AVI, and other video formats
* Automatic speech-to-text transcription
* Subtitle generation in SRT format
* FastAPI backend processing
* Simple Flet GUI frontend
* Multi-language support

---

## System Requirements

### Operating System

* Windows 10 / Windows 11

### Software Requirements

* Python 3.10 - 3.12
* FFmpeg
* Git (optional)

### Hardware Requirements

Minimum:

* Intel i3 / Ryzen 3
* 8 GB RAM
* 5 GB Free Storage

Recommended:

* Intel i5 / Ryzen 5+
* 16 GB RAM
* SSD Storage

---

## Project Structure

backend/
│
├── main.py
├── requirements.txt
│
app/
│
├── main.py
├── requirements.txt

---

## Installation

### Create Virtual Environment

Backend

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Frontend

```cmd
cd app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## Install FFmpeg

Download FFmpeg and add it to PATH.

Verify:

```cmd
ffmpeg -version
```

---

## Start Backend

```cmd
cd backend
.venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Start Frontend

```cmd
cd app
.venv\Scripts\activate
python main.py
```

---

## Dependency List

Frontend

* flet
* requests

Backend

* fastapi
* uvicorn
* python-multipart
* openai-whisper
* ffmpeg-python

---

## Safety Checks

Before running:

1. Verify Python installation.
2. Verify FFmpeg installation.
3. Verify backend dependencies.
4. Verify frontend dependencies.
5. Verify virtual environment activation.
6. Verify port 8000 availability.

---

## Troubleshooting

### FFmpeg Not Found

```cmd
ffmpeg -version
```

If command not found, add FFmpeg to PATH.

### Whisper Installation Error

```cmd
pip install openai-whisper
```

### Backend Not Reachable

Verify:

```cmd
http://127.0.0.1:8000/docs
```

---

## Security Notes

* Run only trusted video files.
* Keep dependencies updated.
* Use virtual environments.
* Do not expose backend publicly without authentication.
