#!/usr/bin/env python3
"""
Image Resize Application
A command-line tool for resizing images with various options including
aspect ratio preservation, batch processing, and multiple output formats.

Author: Claude
Version: 1.0.0
Python: 3.8+
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Tuple, List, Optional
import unittest

try:
    from PIL import Image, ImageOps
except ImportError:
    print("Error: Pillow library is required. Install with: pip install Pillow")
    sys.exit(1)


class ImageResizer:
    """Main class for handling image resize operations."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'}
    
    def __init__(self):
        self.processed_count = 0
        self.failed_count = 0
    
    def resize_image(self, input_path: str, output_path: str, width: int, height: int, 
                    maintain_aspect: bool = True, quality: int = 95) -> bool:
        """
        Resize a single image.
        
        Args:
            input_path: Path to input image
            output_path: Path to save resized image
            width: Target width
            height: Target height
            maintain_aspect: Whether to maintain aspect ratio
            quality: JPEG quality (1-100)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate input file
            if not os.path.exists(input_path):
                print(f"Error: Input file '{input_path}' not found")
                return False
            
            # Check if file is a supported image format
            if not self._is_supported_format(input_path):
                print(f"Error: Unsupported file format for '{input_path}'")
                return False
            
            # Open and resize image
            with Image.open(input_path) as img:
                # Convert RGBA to RGB for JPEG output if needed
                if img.mode in ('RGBA', 'LA') and output_path.lower().endswith(('.jpg', '.jpeg')):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Calculate new dimensions
                if maintain_aspect:
                    # Use thumbnail method to maintain aspect ratio
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                    new_width, new_height = img.size
                else:
                    # Force exact dimensions
                    img = img.resize((width, height), Image.Resampling.LANCZOS)
                    new_width, new_height = width, height
                
                # Create output directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Save the resized image
                save_kwargs = {}
                if output_path.lower().endswith(('.jpg', '.jpeg')):
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                
                img.save(output_path, **save_kwargs)
                
                print(f"✓ Resized '{input_path}' to {new_width}x{new_height} -> '{output_path}'")
                self.processed_count += 1
                return True
                
        except Exception as e:
            print(f"✗ Failed to resize '{input_path}': {str(e)}")
            self.failed_count += 1
            return False
    
    def batch_resize(self, input_dir: str, output_dir: str, width: int, height: int,
                    maintain_aspect: bool = True, quality: int = 95) -> None:
        """
        Resize all images in a directory.
        
        Args:
            input_dir: Directory containing input images
            output_dir: Directory to save resized images
            width: Target width
            height: Target height
            maintain_aspect: Whether to maintain aspect ratio
            quality: JPEG quality (1-100)
        """
        if not os.path.exists(input_dir):
            print(f"Error: Input directory '{input_dir}' not found")
            return
        
        # Find all image files
        image_files = []
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if self._is_supported_format(file):
                    image_files.append(os.path.join(root, file))
        
        if not image_files:
            print(f"No supported image files found in '{input_dir}'")
            return
        
        print(f"Found {len(image_files)} image(s) to process...")
        
        # Process each image
        for input_path in image_files:
            # Create relative output path
            rel_path = os.path.relpath(input_path, input_dir)
            output_path = os.path.join(output_dir, rel_path)
            
            self.resize_image(input_path, output_path, width, height, maintain_aspect, quality)
    
    def _is_supported_format(self, filename: str) -> bool:
        """Check if file has a supported image format."""
        return Path(filename).suffix.lower() in self.SUPPORTED_FORMATS
    
    def get_image_info(self, image_path: str) -> Optional[Tuple[int, int, str]]:
        """
        Get basic information about an image.
        
        Returns:
            Tuple of (width, height, format) or None if error
        """
        try:
            with Image.open(image_path) as img:
                return img.size[0], img.size[1], img.format
        except Exception:
            return None


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Resize images while maintaining quality and aspect ratio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Resize single image to 800x600 (maintain aspect ratio)
  python main.py -i photo.jpg -o resized_photo.jpg -w 800 -h 600
  
  # Resize image to exact dimensions (ignore aspect ratio)
  python main.py -i photo.jpg -o resized_photo.jpg -w 800 -h 600 --no-aspect
  
  # Batch resize all images in a folder
  python main.py -i ./photos -o ./resized_photos -w 1920 -h 1080
  
  # Get image information
  python main.py -i photo.jpg --info
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                       help='Input image file or directory')
    parser.add_argument('-o', '--output',
                       help='Output image file or directory')
    parser.add_argument('-w', '--width', type=int,
                       help='Target width in pixels')
    parser.add_argument('-h', '--height', type=int,
                       help='Target height in pixels')
    parser.add_argument('--no-aspect', action='store_true',
                       help='Do not maintain aspect ratio')
    parser.add_argument('-q', '--quality', type=int, default=95,
                       help='JPEG quality (1-100, default: 95)')
    parser.add_argument('--info', action='store_true',
                       help='Show image information only')
    
    return parser


def validate_arguments(args) -> bool:
    """Validate command-line arguments."""
    if args.info:
        return True  # Only need input for info mode
    
    if not args.output:
        print("Error: Output path is required")
        return False
    
    if not args.width or not args.height:
        print("Error: Both width and height are required")
        return False
    
    if args.width <= 0 or args.height <= 0:
        print("Error: Width and height must be positive integers")
        return False
    
    if not (1 <= args.quality <= 100):
        print("Error: Quality must be between 1 and 100")
        return False
    
    return True


def main():
    """Main function to handle command-line interface."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if not validate_arguments(args):
        return 1
    
    resizer = ImageResizer()
    
    # Info mode - just show image information
    if args.info:
        if os.path.isfile(args.input):
            info = resizer.get_image_info(args.input)
            if info:
                width, height, fmt = info
                print(f"Image: {args.input}")
                print(f"Dimensions: {width} x {height} pixels")
                print(f"Format: {fmt}")
                print(f"File size: {os.path.getsize(args.input) / 1024:.1f} KB")
            else:
                print(f"Error: Could not read image info from '{args.input}'")
                return 1
        else:
            print("Error: Info mode requires a single image file")
            return 1
        return 0
    
    # Resize mode
    if os.path.isfile(args.input):
        # Single file resize
        success = resizer.resize_image(
            args.input, args.output, args.width, args.height,
            maintain_aspect=not args.no_aspect, quality=args.quality
        )
        return 0 if success else 1
    
    elif os.path.isdir(args.input):
        # Batch resize
        resizer.batch_resize(
            args.input, args.output, args.width, args.height,
            maintain_aspect=not args.no_aspect, quality=args.quality
        )
        
        print(f"\nProcessing complete:")
        print(f"✓ Successfully processed: {resizer.processed_count}")
        print(f"✗ Failed: {resizer.failed_count}")
        return 0 if resizer.failed_count == 0 else 1
    
    else:
        print(f"Error: Input path '{args.input}' is not a valid file or directory")
        return 1


# Simple unit tests
class TestImageResizer(unittest.TestCase):
    """Basic unit tests for ImageResizer class."""
    
    def setUp(self):
        self.resizer = ImageResizer()
    
    def test_supported_format_check(self):
        """Test supported format detection."""
        self.assertTrue(self.resizer._is_supported_format('test.jpg'))
        self.assertTrue(self.resizer._is_supported_format('test.PNG'))
        self.assertFalse(self.resizer._is_supported_format('test.txt'))
        self.assertFalse(self.resizer._is_supported_format('test.pdf'))
    
    def test_initialization(self):
        """Test class initialization."""
        self.assertEqual(self.resizer.processed_count, 0)
        self.assertEqual(self.resizer.failed_count, 0)
    
    def test_supported_formats_exist(self):
        """Test that supported formats are defined."""
        self.assertIsInstance(self.resizer.SUPPORTED_FORMATS, set)
        self.assertGreater(len(self.resizer.SUPPORTED_FORMATS), 0)


def run_tests():
    """Run the unit tests."""
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == '__main__':
    # Uncomment the line below to run tests
    # run_tests()
    
    # Run main application
    sys.exit(main())
