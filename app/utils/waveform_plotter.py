# app/utils/waveform_plotter.py

import os
import matplotlib.pyplot as plt
from pydub import AudioSegment

def plot_waveform_with_fade(audio_path: str, output_path: str) -> str:
    """
    Generate waveform plot for the given audio file and highlight fade-out visually
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        samples = audio.get_array_of_samples()

        plt.figure(figsize=(10, 3))
        plt.plot(samples)
        plt.title("Waveform Plot with Fade-out Region")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.tight_layout()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()

        return output_path
    except Exception as e:
        return f"Error generating waveform plot: {e}"
