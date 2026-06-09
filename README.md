# 🎬 Video Subtitle Generator

A desktop application that automatically generates subtitle (.srt) files from video files using OpenAI Whisper. The project consists of a FastAPI backend for transcription processing and a Flet frontend for a simple user interface.

---

# Features

* Generate subtitles from video files
* Supports MP4, MKV, AVI, MOV and other common video formats
* Automatic speech-to-text conversion using Whisper
* Generates industry-standard SRT subtitle files
* Simple graphical user interface built with Flet
* FastAPI backend for subtitle processing
* Local processing (no cloud upload required)

---

# Project Structure

```text
subtitle-generator/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── uploads/
│
├── app/
│   ├── main.py
│   └── requirements.txt
│
├── README.md
├── .gitignore
└── check_environment.bat
```

---

# Technology Stack

## Frontend

* Python
* Flet
* Requests

## Backend

* FastAPI
* Uvicorn
* OpenAI Whisper
* FFmpeg
* Python Multipart

---

# Prerequisites

Before running the project, install:

* Python 3.10 or newer
* FFmpeg
* Git

---

# Installing FFmpeg

Download FFmpeg from the official website:

https://ffmpeg.org/download.html

Verify installation:

```bash
ffmpeg -version
```

---

# Backend Setup

Navigate to backend folder:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start backend server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Navigate to frontend folder:

```bash
cd app
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run application:

```bash
python main.py
```

---

# How to Use

1. Start the FastAPI backend.
2. Launch the Flet application.
3. Select a video file.
4. Upload the file.
5. Wait for transcription to complete.
6. Download the generated subtitle (.srt) file.

---

# Supported Formats

### Video

* MP4
* MKV
* AVI
* MOV
* WMV
* WEBM

### Output

* SRT (SubRip Subtitle)

---

# Development Environment

Tested On:

* Windows 10
* Windows 11
* Python 3.12
* FFmpeg 7.x

---

# Security Recommendations

* Run the application inside a virtual environment.
* Keep dependencies updated.
* Process only trusted video files.
* Do not expose the FastAPI server directly to the internet without authentication.

---

# Troubleshooting

## FFmpeg Not Found

Check:

```bash
ffmpeg -version
```

Add FFmpeg to system PATH if not detected.

---

## Backend Connection Error

Verify backend is running:

```text
http://127.0.0.1:8000/docs
```

---

## Missing Dependencies

Install all packages:

```bash
pip install -r requirements.txt
```

---

# Git Ignore

Recommended entries:

```gitignore
.venv/
venv/
__pycache__/
*.pyc
.env
.vscode/
build/
dist/
uploads/
```

---

# License

This project is provided for educational and personal use.

---

# Author

Hari Kumaran

Built using Python, FastAPI, Flet, Whisper, and FFmpeg.
