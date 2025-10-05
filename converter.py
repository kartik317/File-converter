from PIL import Image
import os

def convert_image(input_path, output_format, output_path=None):
    """
    Convert an image file to a specified format.
    
    Args:
        input_path (str): Path to the input image file
        output_format (str): Target format - one of ["png", "jpg", "jpeg", "webp"]
        output_path (str, optional): Path for the output file. If None, creates a new file
                                      with the same name but different extension
    
    Returns:
        str: Path to the converted image file
    
    Raises:
        ValueError: If output_format is not supported
        FileNotFoundError: If input_path doesn't exist
    """
    # Validate output format
    supported_formats = ["png", "jpg", "jpeg", "webp"]
    output_format = output_format.lower()
    
    if output_format not in supported_formats:
        raise ValueError(f"Unsupported format: {output_format}. Must be one of {supported_formats}")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Generate output path if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.{output_format}"
    
    # Open and convert the image
    with Image.open(input_path) as img:
        # Convert RGBA to RGB for formats that don't support transparency (jpg, jpeg)
        if output_format in ["jpg", "jpeg"] and img.mode in ("RGBA", "LA", "P"):
            # Create a white background
            rgb_img = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
            img = rgb_img
        
        # Save the image
        if output_format in ["jpg", "jpeg"]:
            img.save(output_path, format="JPEG")
        elif output_format == "png":
            img.save(output_path, format="PNG")
        elif output_format == "webp":
            img.save(output_path, format="WEBP")
    
    return output_path

import subprocess
import os

def convert_video(input_path, output_format, output_path=None):
    """
    Convert a video file to a specified format or extract audio as MP3.
    
    Args:
        input_path (str): Path to the input video file
        output_format (str): Target format - one of ["mp4", "mkv", "avi", "mov", "mp3"]
        output_path (str, optional): Path for the output file. If None, creates a new file
                                      with the same name but different extension
    
    Returns:
        str: Path to the converted video/audio file
    
    Raises:
        ValueError: If output_format is not supported
        FileNotFoundError: If input_path doesn't exist or ffmpeg is not installed
        RuntimeError: If conversion fails
    """
    # Validate output format
    supported_formats = ["mp4", "mkv", "avi", "mov", "mp3"]
    output_format = output_format.lower()
    
    if output_format not in supported_formats:
        raise ValueError(f"Unsupported format: {output_format}. Must be one of {supported_formats}")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Check if ffmpeg is installed
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise FileNotFoundError("ffmpeg is not installed. Please install ffmpeg to use this function.")
    
    # Generate output path if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.{output_format}"
    
    # Build ffmpeg command based on output format
    if output_format == "mp3":
        # Extract audio only
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vn",  # No video
            "-acodec", "libmp3lame",
            "-y",  # Overwrite output file
            output_path
        ]
    elif output_format == "mp4":
        command = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-y",
            output_path
        ]
    elif output_format == "mkv":
        command = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "copy",
            "-c:a", "copy",
            "-y",
            output_path
        ]
    elif output_format == "avi":
        command = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "mpeg4",
            "-c:a", "libmp3lame",
            "-y",
            output_path
        ]
    elif output_format == "mov":
        command = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-y",
            output_path
        ]
    
    # Run ffmpeg command
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Conversion failed: {e.stderr}")
    
import subprocess
import os

def convert_audio(input_path, output_format, output_path=None):
    """
    Convert an audio file to a specified format.
    
    Args:
        input_path (str): Path to the input audio file
        output_format (str): Target format - one of ["mp3", "wav", "ogg", "m4a"]
        output_path (str, optional): Path for the output file. If None, creates a new file
                                      with the same name but different extension
    
    Returns:
        str: Path to the converted audio file
    
    Raises:
        ValueError: If output_format is not supported
        FileNotFoundError: If input_path doesn't exist or ffmpeg is not installed
        RuntimeError: If conversion fails
    """
    # Validate output format
    supported_formats = ["mp3", "wav", "ogg", "m4a"]
    output_format = output_format.lower()
    
    if output_format not in supported_formats:
        raise ValueError(f"Unsupported format: {output_format}. Must be one of {supported_formats}")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Check if ffmpeg is installed
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise FileNotFoundError("ffmpeg is not installed. Please install ffmpeg to use this function.")
    
    # Generate output path if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.{output_format}"
    
    # Build ffmpeg command based on output format
    if output_format == "mp3":
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vn",  # No video
            "-acodec", "libmp3lame",
            "-y",  # Overwrite output file
            output_path
        ]
    elif output_format == "wav":
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-y",
            output_path
        ]
    elif output_format == "ogg":
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vn",
            "-acodec", "libvorbis",
            "-y",
            output_path
        ]
    elif output_format == "m4a":
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vn",
            "-acodec", "aac",
            "-y",
            output_path
        ]
    
    # Run ffmpeg command
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Conversion failed: {e.stderr}")

'''
# Example usage
if __name__ == "__main__":
    # Convert audio to MP3
    try:
        output = convert_audio("Nemure.mp3", "ogg")
        print(f"Audio converted successfully: {output}")
    except Exception as e:
        print(f"Error: {e}")'''
