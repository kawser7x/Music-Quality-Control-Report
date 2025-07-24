core/waveform_plotter.py

import os import matplotlib.pyplot as plt import numpy as np from pydub import AudioSegment

def plot_waveform(audio_path: str, output_path: str): try: # Load audio audio = AudioSegment.from_file(audio_path)

# Convert to mono
    audio = audio.set_channels(1)

    # Get samples as numpy array
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate

    # Generate time axis
    duration = len(audio) / 1000.0  # milliseconds to seconds
    time = np.linspace(0., duration, num=len(samples))

    # Plot
    plt.figure(figsize=(10, 3))
    plt.plot(time, samples, linewidth=0.7, color='gray')
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    return True

except Exception as e:
    print(f"Error in plot_waveform: {e}")
    return False