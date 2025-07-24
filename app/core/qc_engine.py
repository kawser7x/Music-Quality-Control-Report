import os
import numpy as np
import pyloudnorm as pyln
from pydub import AudioSegment
import matplotlib.pyplot as plt
from app.utils.waveform_plotter import generate_waveform_plot

def analyze_audio(file_path: str) -> dict:
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)

    # Loudness analysis
    meter = pyln.Meter(audio.frame_rate)
    loudness = meter.integrated_loudness(samples)
    true_peak = np.max(samples) / (2 ** 15)
    duration_sec = len(audio) / 1000.0

    # Fade-out check: between last 8-15 seconds
    fade_start = max(0, duration_sec - 15)
    fade_end = max(0, duration_sec - 8)
    fade_region = audio[fade_start * 1000: fade_end * 1000]
    fade_samples = np.array(fade_region.get_array_of_samples()).astype(np.float32)
    fade_db = 20 * np.log10(np.maximum(np.abs(fade_samples), 1e-10))
    fade_slope = np.polyfit(range(len(fade_db)), fade_db, 1)[0]

    has_fade_out = fade_slope < 0  # Negative slope means fading out

    # Waveform plot
    plot_path = "app/static/waveform/waveform_plot.png"
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    generate_waveform_plot(file_path, plot_path)

    # Report (Bangla + English)
    result_bn = []
    result_en = []

    # Loudness check
    if -15 <= loudness <= -13:
        result_bn.append(f"🔊 লাউডনেস ঠিক আছে: {loudness:.2f} LUFS")
        result_en.append(f"🔊 Loudness is within range: {loudness:.2f} LUFS")
    else:
        result_bn.append(f"⚠️ লাউডনেস ভুল: {loudness:.2f} LUFS (চাহিদা -14 ±1)")
        result_en.append(f"⚠️ Loudness out of range: {loudness:.2f} LUFS (Target -14 ±1)")

    # True peak
    if true_peak <= 1.0:
        result_bn.append(f"✅ ট্রু পিক ঠিক আছে: {true_peak:.2f} dBFS")
        result_en.append(f"✅ True peak is okay: {true_peak:.2f} dBFS")
    else:
        result_bn.append(f"❌ ট্রু পিক বেশি: {true_peak:.2f} dBFS")
        result_en.append(f"❌ True peak too high: {true_peak:.2f} dBFS")

    # Fade-out
    if has_fade_out:
        result_bn.append("✅ ফেইড-আউট ঠিকমতো আছে (শেষ ৮-১৫ সেকেন্ডের মধ্যে)")
        result_en.append("✅ Fade-out detected properly (within last 8–15 sec)")
    else:
        result_bn.append("❌ ফেইড-আউট পাওয়া যায়নি")
        result_en.append("❌ No fade-out detected")

    return {
        "report_bn": "\n".join(result_bn),
        "report_en": "\n".join(result_en),
        "waveform_plot": "/static/waveform/waveform_plot.png"
    }