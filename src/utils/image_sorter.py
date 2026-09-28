from PIL import Image, UnidentifiedImageError
import os
import shutil
import requests
from urllib.parse import urlparse
import glob

def download_image(url, save_dir):
    """Download image from URL to specified directory and return local path."""
    filename = os.path.basename(urlparse(url).path) or f"image_{hash(url)}.jpg"
    local_path = os.path.join(save_dir, filename) 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return local_path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

def process_image(path, formats, original_path=None):
    """Determine image format and add to appropriate category in formats dictionary."""
    path_to_record = original_path if original_path else path
    try:
        with Image.open(path) as img:
            fmt = img.format.lower() if img.format else "unknown"
            formats.setdefault(fmt, []).append(path_to_record)
    except UnidentifiedImageError:
        if path.lower().endswith('.svg'):
            formats.setdefault("svg", []).append(path_to_record)
    except Exception as e:
        print(f"Error processing {path}: {e}")

def handle_image_path(path, formats, temp_dir):
    """Process image from URL or local path and categorize by format."""
    if path.startswith(('http://', 'https://')):
        local_path = download_image(path, temp_dir)
        if local_path:
            process_image(local_path, formats, original_path=path)
    else:
        process_image(path, formats)

def sorted_images():
    """Move formatted files to sorted_images directory."""
    output_dir = "sorted_images"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    for file in glob.glob("*_files.txt"):
        if file not in ("javascript_files.txt", "css_files.txt"):
            shutil.move(file, os.path.join(output_dir, file))

def process_image_collection(image_paths):
    """Process images and return categorized formats."""
    formats = {}
    temp_dir = "temp_downloads"
    os.makedirs(temp_dir, exist_ok=True)
    for path in image_paths:
        handle_image_path(path, formats, temp_dir)
    for fmt, images in formats.items():
        with open(f"{fmt}_files.txt", "w") as f:
            for img in images:
                f.write(f"{img}\n")  
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    return formats

def sort_images_by_format(image_paths):
    """Categorize images by format and save results to text files."""
    formats = process_image_collection(image_paths)  
    sorted_images() 
    print(f"Images categorized by format:")
    for fmt, count in {fmt: len(imgs) for fmt, imgs in formats.items()}.items():
        print(f"  - {fmt}: {count} images")