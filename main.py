import uuid
from scipy.io.wavfile import write
from PIL import Image
import numpy as np
import os
import wave


def rgb_to_frequency(rgb_value):
    """Convert RGB value to frequency."""
    r, g, b = rgb_value
    # Use the average of RGB values as frequency
    return (r + g + b) / 3


def generate_sound(frequency, duration=100):
    """Generate sound of given frequency and duration."""
    sample_rate = 44100  # 44.1 kHz
    num_samples = int(sample_rate * duration / 1000)

    # Generate a sound wave with the specified frequency
    t = np.linspace(0, duration / 1000, num_samples, endpoint=False)
    sound_wave = 4096 * np.sin(2 * np.pi * frequency * t)

    # Save the sound wave to a .wav file
    filename = f'temp_{uuid.uuid4().hex}.wav'
    write(filename, sample_rate, sound_wave.astype(np.int16))
    return filename


def concatenate_sounds(filenames, output_filename):
    """Concatenate a list of sound files into a single file."""
    data = []
    for filename in filenames:
        w = wave.open(filename, 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(output_filename, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()


def main(image_path,n):
    # Open the image using PIL
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    width, height = img.size
    block_size = n

    # Process the image in 8x8 blocks
    filenames = []
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # Calculate average frequency of each block
            total_freq = 0
            for dx in range(block_size):
                for dy in range(block_size):
                    # Get RGB value of each pixel
                    r, g, b = pixels[x + dx, y + dy]

                    # Convert RGB to frequency
                    frequency = rgb_to_frequency((r, g, b))
                    total_freq += frequency

            avg_freq = total_freq / (block_size * block_size)

            # Generate sound
            filename = generate_sound(avg_freq)
            filenames.append(filename)

    # Concatenate all sounds into a single file
    concatenate_sounds(filenames, 'output.wav')

    # Remove temporary sound files
    for filename in filenames:
        os.remove(filename)


if __name__ == "__main__":
    # Replace with your image path
    image_path = ""
    block_size = 32
    main(image_path,block_size)
