# File Converter Web App

![File converter](https://i.postimg.cc/QCtw0Yf8/favicon.jpg)

A modern Flask-based web application for converting images, videos, and audio files between popular formats. Features a clean UI, loading spinners, and automatic file cleanup.

## Features
- Convert images (PNG, JPG, JPEG, WEBP)
- Convert videos (MP4, MKV, AVI, MOV, extract MP3 audio)
- Convert audio (MP3, WAV, OGG, M4A)
- Upload files up to 100MB
- Loading spinner during upload and conversion
- Automatic cleanup of old files
- Responsive, modern design

## Getting Started

### Prerequisites
- Python 3.13+
- FFmpeg (for video/audio conversion)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kartik317/File-converter.git
   cd File-converter
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure FFmpeg is installed and available in your PATH.
   ```bash
   ffmpeg -version
   ```

### Running Locally
```bash
python app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

### Deployment
- The app is ready for deployment on platforms like Heroku (see `Procfile`).
- For production, use Gunicorn:
  ```bash
  gunicorn app:app
  ```
- Full app is already deployed on render [File converter](https://file-converter-fwsy.onrender.com)

## Usage
1. Go to the home page and upload a file.
2. Select the desired output format on the converter page.
3. Click "Convert" to download the converted file.

## Project Structure
```
├── app.py
├── converter.py
├── utils.py
├── requirements.txt
├── procfile
├── static/
|   ├── assets/
|   |   ├── favicon.jpg
│   ├── styles/
│   │   ├── homestyles.css
│   │   └── converterstyles.css
│   ├── scripts/
│   │   └── script.js
├── templates/
│   ├── base.html
│   ├── home.html
│   └── converterPage.html
└── uploads/
```

## Author
Kartik317
