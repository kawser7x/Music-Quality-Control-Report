# 🎧 # TrackVerify: Music Quality Control Report (OFFSTEP v2.2)

[![Live Demo](https://img.shields.io/badge/Live-Demo-green?style=for-the-badge&logo=fastapi)](https://music-quality-control-report-c8uk.onrender.com)
[![Built with FastAPI](https://img.shields.io/badge/Built%20with-FastAPI-blue?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🔥 **TrackVerify** is a professional-level, dual-language (বাংলা+English) music audio quality control system built to ensure 100% compliance with **OFFSTEP v2.2 submission standards** for music distribution.

---

## 🚀 Features

✅ OFFSTEP v2.2 Audio QC  
✅ Dual-Language QC Reports (বাংলা + English)  
✅ Waveform Fade-Out Detection with Plot  
✅ PDF Report Download  
✅ Live UI Preview + Result Copy  
✅ ACRCloud + AudD Copyright Checker  
✅ No Login Needed — Fully Personal  
✅ Stylish Dark Mode UI  
✅ FastAPI + Jinja2 + JS Powered  
✅ Render Deployment Ready

---

## 🌐 Live Demo

🔗 [https://music-quality-control-report-c8uk.onrender.com](https://music-quality-control-report-c8uk.onrender.com)

---

## 📷 UI Preview

> Modern, professional, dual-language UI with dark mode:

![TrackVerify UI](https://raw.githubusercontent.com/kawser7x/Music-Quality-Control-Report/main/static/assets/trackverify_ui_preview.png)

---

## 📂 Project Structure

```
app/
├── core/
│   ├── qc_engine.py
│   ├── copyright_checker.py
├── routes/
│   ├── main.py
│   ├── upload_audio.py
│   ├── pdf_generator.py
│   ├── health.py
├── templates/
│   ├── index.html
│   ├── result.html
├── static/
│   ├── css/styles.css
│   ├── js/script.js
│   └── assets/
├── utils/
│   └── waveform_plotter.py
config/
│   └── qc_profiles.yaml (optional)
scripts/
│   └── sample_audio_generator.py (optional)
tests/
│   └── test_qc_engine.py
Dockerfile
requirements.txt
README.md
```

---

## 🔍 Routes

| Method | Route             | Description                      |
|--------|------------------|----------------------------------|
| GET    | `/`              | Upload UI Page                   |
| POST   | `/upload-audio/` | Analyze Audio QC + Copyright     |
| GET    | `/generate-pdf/` | Generate Downloadable PDF Report |
| GET    | `/healthz`       | Render Health Check              |

---

## ⚙️ Tech Stack

- **Backend:** FastAPI, Jinja2, ffmpeg-python, pydub, pyloudnorm, mutagen  
- **Frontend:** HTML5, CSS3, JS (Copy + PDF), Waveform Visualization  
- **APIs:** ACRCloud, AudD  
- **Deployment:** Render + Docker  
- **Language:** Dual (Bengali 🇧🇩 + English 🇺🇸)

---

## 📥 Installation

```bash
git clone https://github.com/kawser7x/Music-Quality-Control-Report.git
cd Music-Quality-Control-Report
pip install -r requirements.txt
uvicorn app.main:app --reload
```

📝 Requires: `ffmpeg` installed and available in system path.

---

## 🧪 Test (Optional)

```bash
pytest tests/test_qc_engine.py
```

---

## 👤 Contact

Reach out for issues, feedback, or collaborations:

- 📧 Email: godzulfi@gmail.com  
- 🐦 Twitter: [@kawser7x](https://twitter.com/kawser7x)  
- 💬 Telegram: [@kawser7x](https://t.me/kawser7x)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

⭐ **Built with ❤️ for music creators to get 100% approval on OFFSTEP submissions.**
