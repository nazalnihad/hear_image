from PIL import Image

def encode_text(text, output_filename):
    # Convert the text to bytes
    text_bytes = text.encode()

    # Calculate the size of the image based on the length of the text
    image_width = int(len(text_bytes) ** 0.5) + 1
    image_height = (len(text_bytes) // image_width) + 1

    # Create a new image with higher resolution and more colors
    image = Image.new("RGB", (image_width, image_height))

    # Encode the text into the image pixels
    pixels = []
    for byte in text_bytes:
        pixels.append((byte, byte, byte))  # Use grayscale by repeating the byte three times
    image.putdata(pixels)

    # Save the image with higher quality
    image.save(output_filename, quality=95)  # Use higher quality setting
    print(f"Image saved as {output_filename}")

def decode_image(image_filename):
    # Open the image
    image = Image.open(image_filename)

    # Get the pixel values
    pixels = list(image.getdata())

    # Decode the text from the pixel values
    text_bytes = bytes(pixel[0] for pixel in pixels)
    decoded_text = text_bytes.decode()

    # Print the decoded text
    print(f"Decoded text: {decoded_text}")

def main():
    choice = input("Enter 'e' to encode text or 'd' to decode an image: ")

    if choice.lower() == 'e':
        user_input = input("Enter your text: ")
        output_filename = "encoded.png"
        encode_text(user_input, output_filename)
    elif choice.lower() == 'd':
        image_filename = input("Enter the image filename: ")
        decode_image(image_filename)
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
