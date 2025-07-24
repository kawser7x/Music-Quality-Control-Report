# core/qc_engine.py

import io
import pyloudnorm as pyln
import soundfile as sf
from pydub import AudioSegment

def analyze_loudness(file: bytes):
    try:
        # Load audio with PyDub
        audio = AudioSegment.from_file(io.BytesIO(file))
        audio = audio.set_channels(2).set_frame_rate(44100)

        # Export to raw WAV for pyloudnorm
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        # Read with soundfile
        data, rate = sf.read(wav_io)

        # Analyze loudness
        meter = pyln.Meter(rate)
        loudness = meter.integrated_loudness(data)

        # Evaluate compliance
        target_lufs = -14.0
        min_lufs = -15.5
        max_lufs = -13.0

        status = "PASS" if min_lufs <= loudness <= max_lufs else "FAIL"

        # Prepare bilingual result
        report = f"""
1. 🎚️ Audio Quality – Loudness

   English:
   • Measured Loudness: {loudness:.2f} LUFS
   • Target: -14.0 ±1.5 LUFS
   • Result: {"✅ PASS" if status == "PASS" else "❌ FAIL"}

   বাংলা:
   • পরিমাপ করা লাউডনেস: {loudness:.2f} LUFS
   • লক্ষ্য: -14.0 ±1.5 LUFS
   • ফলাফল: {"✅ পাস" if status == "PASS" else "❌ ফেল"}
"""
        return report.strip()

    except Exception as e:
        return f"❌ Error analyzing loudness: {str(e)}"