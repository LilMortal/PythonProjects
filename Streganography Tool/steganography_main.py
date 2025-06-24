#!/usr/bin/env python3
"""
Steganography Tool - Hide and Extract Text Messages in Images
============================================================

This tool implements LSB (Least Significant Bit) steganography to hide text messages
within image files. It supports both encoding (hiding) and decoding (extracting) messages.

Author: Claude AI
Version: 1.0
Python Version: 3.8+
"""

import os
import sys
import argparse
from PIL import Image
import numpy as np
from typing import Optional, Tuple


class SteganographyError(Exception):
    """Custom exception for steganography operations"""
    pass


class SteganographyTool:
    """
    A class to handle steganographic operations on images.
    
    This class provides methods to hide text messages in images using LSB steganography
    and extract hidden messages from images.
    """
    
    def __init__(self):
        self.delimiter = "###END###"  # Delimiter to mark end of hidden message
    
    def _text_to_binary(self, text: str) -> str:
        """Convert text to binary representation"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    def _binary_to_text(self, binary: str) -> str:
        """Convert binary representation back to text"""
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def _get_image_capacity(self, image_path: str) -> int:
        """Calculate maximum characters that can be hidden in the image"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if not already
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                width, height = img.size
                # Each pixel has 3 channels (RGB), each can hide 1 bit
                # 8 bits per character, so capacity = (width * height * 3) / 8
                return (width * height * 3) // 8
        except Exception as e:
            raise SteganographyError(f"Error calculating image capacity: {str(e)}")
    
    def hide_message(self, image_path: str, message: str, output_path: str) -> bool:
        """
        Hide a text message in an image using LSB steganography.
        
        Args:
            image_path (str): Path to the input image
            message (str): Text message to hide
            output_path (str): Path for the output image with hidden message
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            SteganographyError: If operation fails
        """
        try:
            # Validate input
            if not os.path.exists(image_path):
                raise SteganographyError(f"Input image not found: {image_path}")
            
            if not message.strip():
                raise SteganographyError("Message cannot be empty")
            
            # Add delimiter to mark end of message
            full_message = message + self.delimiter
            
            # Check if message can fit in image
            capacity = self._get_image_capacity(image_path)
            if len(full_message) > capacity:
                raise SteganographyError(
                    f"Message too long! Image can hold {capacity} characters, "
                    f"but message is {len(full_message)} characters"
                )
            
            # Load and prepare image
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Convert image to numpy array for easier manipulation
                img_array = np.array(img)
                
                # Convert message to binary
                binary_message = self._text_to_binary(full_message)
                message_index = 0
                
                # Hide message in image pixels
                for i in range(img_array.shape[0]):  # Height
                    for j in range(img_array.shape[1]):  # Width
                        for k in range(3):  # RGB channels
                            if message_index < len(binary_message):
                                # Modify LSB of current pixel channel
                                img_array[i, j, k] = (img_array[i, j, k] & 0xFE) | int(binary_message[message_index])
                                message_index += 1
                            else:
                                # Message fully encoded
                                break
                        if message_index >= len(binary_message):
                            break
                    if message_index >= len(binary_message):
                        break
                
                # Save the modified image
                result_img = Image.fromarray(img_array)
                result_img.save(output_path)
                
                print(f"✅ Message successfully hidden in image!")
                print(f"📁 Output saved to: {output_path}")
                print(f"📊 Message length: {len(message)} characters")
                print(f"📊 Image capacity: {capacity} characters")
                
                return True
                
        except Exception as e:
            raise SteganographyError(f"Error hiding message: {str(e)}")
    
    def extract_message(self, image_path: str) -> Optional[str]:
        """
        Extract a hidden text message from an image.
        
        Args:
            image_path (str): Path to the image containing hidden message
            
        Returns:
            Optional[str]: The extracted message, or None if no message found
            
        Raises:
            SteganographyError: If operation fails
        """
        try:
            # Validate input
            if not os.path.exists(image_path):
                raise SteganographyError(f"Input image not found: {image_path}")
            
            # Load image
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Convert image to numpy array
                img_array = np.array(img)
                
                # Extract binary data from LSBs
                binary_message = ""
                
                for i in range(img_array.shape[0]):  # Height
                    for j in range(img_array.shape[1]):  # Width
                        for k in range(3):  # RGB channels
                            # Extract LSB
                            binary_message += str(img_array[i, j, k] & 1)
                
                # Convert binary to text
                extracted_text = self._binary_to_text(binary_message)
                
                # Look for delimiter to find end of message
                if self.delimiter in extracted_text:
                    message = extracted_text.split(self.delimiter)[0]
                    if message:
                        print(f"✅ Message successfully extracted!")
                        print(f"📊 Message length: {len(message)} characters")
                        return message
                    else:
                        print("❌ No valid message found in image")
                        return None
                else:
                    print("❌ No hidden message found in image")
                    return None
                    
        except Exception as e:
            raise SteganographyError(f"Error extracting message: {str(e)}")


def create_sample_image(filename: str = "sample.png", size: Tuple[int, int] = (800, 600)) -> None:
    """Create a sample image for testing purposes"""
    try:
        # Create a gradient image
        img = Image.new('RGB', size)
        pixels = []
        
        for y in range(size[1]):
            for x in range(size[0]):
                r = int(255 * x / size[0])
                g = int(255 * y / size[1])
                b = int(255 * (x + y) / (size[0] + size[1]))
                pixels.append((r, g, b))
        
        img.putdata(pixels)
        img.save(filename)
        print(f"📸 Sample image created: {filename}")
        
    except Exception as e:
        print(f"❌ Error creating sample image: {str(e)}")


def main():
    """Main function to handle command-line interface"""
    parser = argparse.ArgumentParser(
        description="Steganography Tool - Hide and extract text messages in images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py hide --image sample.png --message "Secret message" --output hidden.png
  python main.py extract --image hidden.png
  python main.py sample  # Create sample image for testing
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Hide command
    hide_parser = subparsers.add_parser('hide', help='Hide a message in an image')
    hide_parser.add_argument('--image', '-i', required=True, help='Input image path')
    hide_parser.add_argument('--message', '-m', required=True, help='Message to hide')
    hide_parser.add_argument('--output', '-o', required=True, help='Output image path')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract message from an image')
    extract_parser.add_argument('--image', '-i', required=True, help='Image path with hidden message')
    
    # Sample command
    sample_parser = subparsers.add_parser('sample', help='Create a sample image for testing')
    sample_parser.add_argument('--filename', '-f', default='sample.png', help='Sample image filename')
    sample_parser.add_argument('--size', '-s', nargs=2, type=int, default=[800, 600], 
                             help='Image size (width height)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    steg_tool = SteganographyTool()
    
    try:
        if args.command == 'hide':
            print("🔒 Hiding message in image...")
            steg_tool.hide_message(args.image, args.message, args.output)
            
        elif args.command == 'extract':
            print("🔍 Extracting message from image...")
            message = steg_tool.extract_message(args.image)
            if message:
                print(f"\n📝 Extracted Message:")
                print(f"'{message}'")
            
        elif args.command == 'sample':
            print("🎨 Creating sample image...")
            create_sample_image(args.filename, tuple(args.size))
            
    except SteganographyError as e:
        print(f"❌ Steganography Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)


# Simple unit tests (can be run separately)
def run_tests():
    """Run basic unit tests for the steganography tool"""
    print("🧪 Running unit tests...")
    
    steg_tool = SteganographyTool()
    
    # Test 1: Text to binary conversion
    test_text = "Hello"
    binary = steg_tool._text_to_binary(test_text)
    converted_back = steg_tool._binary_to_text(binary)
    assert converted_back == test_text, f"Text conversion failed: {converted_back} != {test_text}"
    print("✅ Test 1 passed: Text to binary conversion")
    
    # Test 2: Create sample image and test capacity
    create_sample_image("test_sample.png", (100, 100))
    capacity = steg_tool._get_image_capacity("test_sample.png")
    expected_capacity = (100 * 100 * 3) // 8  # 3750 characters
    assert capacity == expected_capacity, f"Capacity calculation failed: {capacity} != {expected_capacity}"
    print("✅ Test 2 passed: Image capacity calculation")
    
    # Test 3: Hide and extract message
    test_message = "This is a secret test message!"
    steg_tool.hide_message("test_sample.png", test_message, "test_hidden.png")
    extracted = steg_tool.extract_message("test_hidden.png")
    assert extracted == test_message, f"Message extraction failed: {extracted} != {test_message}"
    print("✅ Test 3 passed: Hide and extract message")
    
    # Cleanup
    for file in ["test_sample.png", "test_hidden.png"]:
        if os.path.exists(file):
            os.remove(file)
    
    print("🎉 All tests passed!")


if __name__ == "__main__":
    # Uncomment the line below to run tests instead of main program
    # run_tests()
    main()
