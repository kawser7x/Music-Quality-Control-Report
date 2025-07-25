import os
import pyloudnorm as pyln
import numpy as np
from pydub import AudioSegment
from app.utils.waveform_plotter import plot_waveform_with_fade

def analyze_audio_quality(audio_path: str) -> dict:
    """
    Analyze loudness and fade-out quality of an audio file.
    Returns OFFSTEP v2.2 formatted result with dual-language (Bangla + English).
    """
    try:
        # Load audio
        audio = AudioSegment.from_file(audio_path)
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples /= np.iinfo(audio.array_type).max  # Normalize

        # Loudness analysis
        meter = pyln.Meter(audio.frame_rate)
        loudness = meter.integrated_loudness(samples)

        # Loudness QC check
        loudness_result = {}
        if -15.0 <= loudness <= -13.0:
            loudness_result["status"] = "✅ PASS"
            loudness_result["message_bn"] = "লাউডনেস -14 LUFS এর মধ্যে রয়েছে (স্ট্যান্ডার্ড)।"
            loudness_result["message_en"] = f"Loudness is within standard range: {loudness:.2f} LUFS."
        else:
            loudness_result["status"] = "❌ FAIL"
            loudness_result["message_bn"] = f"লাউডনেস {loudness:.2f} LUFS যা -14 থেকে ±1 এর বাইরে। ঠিক করুন।"
            loudness_result["message_en"] = f"Loudness is {loudness:.2f} LUFS, which is outside the -14 ±1 LUFS standard range."

        # Fade-out QC check
        duration_sec = len(audio) / 1000
        end_trim = audio[-15000:]  # Last 15 seconds
        fade_duration = detect_fade_out(end_trim)

        fade_result = {}
        if 1.0 <= fade_duration <= 3.0 or 8.0 <= fade_duration <= 15.0:
            fade_result["status"] = "✅ PASS"
            fade_result["message_bn"] = f"ফেড-আউট সময় ঠিক আছে ({fade_duration:.2f} সেকেন্ড)।"
            fade_result["message_en"] = f"Fade-out is within correct range: {fade_duration:.2f} seconds."
        else:
            fade_result["status"] = "❌ FAIL"
            fade_result["message_bn"] = f"ফেড-আউট সময় সঠিক না ({fade_duration:.2f} সেকেন্ড)। 1-3 বা 8-15 সেকেন্ডের মধ্যে দিন।"
            fade_result["message_en"] = f"Fade-out duration is {fade_duration:.2f} seconds, which is not within 1-3 or 8–15 seconds range."

        # Waveform plot
        plot_path = os.path.join("static", "waveform_plot.png")
        plot_result = plot_waveform_with_fade(audio_path, plot_path)

        return {
            "audio_path": audio_path,
            "loudness": loudness_result,
            "fade_out": fade_result,
            "waveform_plot_path": plot_path if os.path.exists(plot_path) else None
        }

    except Exception as e:
        return {
            "error": str(e),
            "message_bn": "অডিও বিশ্লেষণ করতে সমস্যা হয়েছে।",
            "message_en": "Error analyzing the audio file."
        }


def detect_fade_out(audio_segment: AudioSegment) -> float:
    """
    Estimate fade-out duration (in seconds) from the end of an audio segment.
    """
    samples = np.array(audio_segment.get_array_of_samples())
    samples = samples.astype(np.float32)
    samples /= np.iinfo(audio_segment.array_type).max

    rms = np.sqrt(np.mean(samples**2))
    threshold = rms * 0.2
    reversed_samples = samples[::-1]

    for i in range(len(reversed_samples)):
        if abs(reversed_samples[i]) > threshold:
            fade_samples = i
            break
    else:
        fade_samples = len(reversed_samples)

    return fade_samples / audio_segment.frame_rate
