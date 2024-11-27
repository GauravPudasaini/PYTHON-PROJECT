import requests
from bs4 import BeautifulSoup
import re
import os
import hashlib

# Define the URL
url = 'https://www.bing.com/images/search?q=images&form=HDRSC3&first=1&cw=1513&ch=738'

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

# Request the page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Create a folder for downloaded images if it doesn’t exist
download_folder = 'class_images'
os.makedirs(download_folder, exist_ok=True)

# Find the image elements
image_elements = soup.find_all('a', class_='iusc')

# Regular expression to extract the murl value
murl_pattern = re.compile(r'"murl":"(http.*?)"')

# Download images
downloaded_count = 0
for idx, img in enumerate(image_elements[:5], start=1):  # Attempting to get the first 50 images
    try:
        # Extract metadata and find the full-size image URL
        metadata = img.get('m')
        if metadata:
            match = murl_pattern.search(metadata)
            if match:
                img_url = match.group(1)  # Get the full-size image URL

                # Generate a unique filename using a hash of the URL to prevent overwriting
                img_hash = hashlib.md5(img_url.encode()).hexdigest()
                img_path = os.path.join(download_folder, f'image_{img_hash}.jpg')

                # Skip download if image already exists
                if not os.path.exists(img_path):
                    img_data = requests.get(img_url).content
                    with open(img_path, 'wb') as handler:
                        handler.write(img_data)
                    print(f"Downloaded {img_path}")
                    downloaded_count += 1
                else:
                    print(f"Image {img_path} already exists, skipping download.")
            else:
                print(f"Full-size URL not found for image_{idx}")
                
    except Exception as e:
        print(f"Failed to download image_{idx}: {e}")

print(f"Total images downloaded: {downloaded_count}")
