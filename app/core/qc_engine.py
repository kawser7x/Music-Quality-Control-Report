import os
from pydub import AudioSegment
import pyloudnorm as pyln
import matplotlib.pyplot as plt
import numpy as np
from app.utils.waveform_plotter import plot_waveform_with_fade

def analyze_audio_quality(file_path: str) -> dict:
    # Load audio
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate

    # Loudness Meter
    meter = pyln.Meter(sample_rate)
    loudness = meter.integrated_loudness(samples.astype(np.float32))

    # True Peak
    peak_db = 20 * np.log10(np.max(np.abs(samples)) / (2 ** (audio.sample_width * 8 - 1)))

    # Duration
    duration_sec = len(audio) / 1000

    # Fade-out detection
    fade_ok = detect_fade_out(samples, sample_rate, duration_sec)

    # Plot waveform with fade-out range
    plot_path = plot_waveform_with_fade(file_path)

    # Generate result
    summary = "Audio passed all checks ✅" if loudness >= -15 and loudness <= -13 and peak_db <= -1.0 and fade_ok else "Issues detected ❌"
    summary_bn = "অডিও সমস্ত পরীক্ষায় উত্তীর্ণ হয়েছে ✅" if summary.endswith("✅") else "অডিওতে কিছু সমস্যা আছে ❌"

    result = {
        "loudness": f"{loudness:.2f} LUFS",
        "peak": f"{peak_db:.2f} dBFS",
        "fade_out": "OK ✅" if fade_ok else "Missing or too late ❌",
        "waveform_plot": plot_path,
        "summary": summary,
        "summary_bn": summary_bn
    }

    return result

def detect_fade_out(samples, sr, duration_sec):
    # Define fade detection zone: 8–15 seconds before end
    end_sec = duration_sec
    start_sec = max(end_sec - 15, 0)
    mid_sec = max(end_sec - 8, 0)

    start_idx = int(start_sec * sr)
    mid_idx = int(mid_sec * sr)

    start_level = np.mean(np.abs(samples[start_idx:mid_idx]))
    end_level = np.mean(np.abs(samples[mid_idx:]))

    if end_level < start_level * 0.5:
        return True
    return False
