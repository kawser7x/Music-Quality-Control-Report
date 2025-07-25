import os
from pydub import AudioSegment
import numpy as np
import pyloudnorm as pyln
from app.utils.waveform_plotter import plot_waveform_with_fade


def analyze_audio_quality(file_path: str) -> dict:
    # Load audio file
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate

    # Loudness analysis
    meter = pyln.Meter(sample_rate)
    loudness = meter.integrated_loudness(samples.astype(np.float32))

    # Peak calculation
    peak_db = 20 * np.log10(np.max(np.abs(samples)) / (2 ** (audio.sample_width * 8 - 1)))

    # Duration
    duration_sec = len(audio) / 1000

    # Fade-out check
    fade_ok = detect_fade_out(samples, sample_rate, duration_sec)

    # Waveform plot
    plot_path = plot_waveform_with_fade(file_path)

    result = {
        "loudness": f"{loudness:.2f} LUFS",
        "peak": f"{peak_db:.2f} dBFS",
        "fade_out": "OK ✅" if fade_ok else "Missing ❌",
        "waveform_plot": plot_path,
        "summary": "Audio QC Passed ✅" if loudness >= -15 and loudness <= -13 and peak_db <= -1.0 and fade_ok else "QC Failed ❌",
        "summary_bn": "QC রিপোর্ট সঠিক ✅" if loudness >= -15 and loudness <= -13 and peak_db <= -1.0 and fade_ok else "QC রিপোর্টে সমস্যা আছে ❌"
    }
    return result


def detect_fade_out(samples, sr, duration_sec):
    # Fade-out should occur in last 8–15s
    end_sec = duration_sec
    start_sec = max(end_sec - 15, 0)
    mid_sec = max(end_sec - 8, 0)

    start_idx = int(start_sec * sr)
    mid_idx = int(mid_sec * sr)

    start_level = np.mean(np.abs(samples[start_idx:mid_idx]))
    end_level = np.mean(np.abs(samples[mid_idx:]))

    return end_level < (start_level * 0.5)
