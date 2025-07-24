# app/utils/waveform_plotter.py

import os
import matplotlib.pyplot as plt
from pydub import AudioSegment

def generate_waveform_plot(audio_path: str, output_path: str = "app/static/waveform_plot.png") -> str:
    """
    Generate waveform plot for the given audio file and save as PNG.
    """
    try:
        audio = AudioSegment.from_file(audio_path)
        samples = audio.get_array_of_samples()

        plt.figure(figsize=(10, 3))
        plt.plot(samples)
        plt.title("Waveform Plot")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.tight_layout()

        # Make sure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close()

        return output_path
    except Exception as e:
        print(f"Waveform plot generation failed: {e}")
        return ""