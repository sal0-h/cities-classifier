import requests
import io
import os, time
import imghdr
import shelve
import pandas as pd
import threading
from PIL import Image

def download_image(download_path, url, name):
    try:
        # Send a GET request to the URL to get the image content
        response = requests.get(url)
        # Raise an exception for bad responses
        response.raise_for_status()
        # Detect image type from the content
        image_type = imghdr.what(None, h=response.content)
        if image_type is None:
            raise ValueError("Could not detect image type")
        # Construct file path with correct extension
        file_path = os.path.join(download_path, f"{name}.{image_type}")
        # Write the image content to a file
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Image {name} downloaded from {url[0:5]} to {file_path}")
    except Exception as e:
        print("Womp womp", e, url)

def download_images(city, images):
    create_folder(f"test/{city}")
    for i, image in enumerate(images):
        if not os.path.exists(f"images_fresh/{city}/{city}{i+1}.jpeg"):
            download_image(f"images_fresh/{city}/", image, f"{city}{i+1}")

def create_folder(name):
    if os.path.exists(f"./{name}"):
        print("Folder already exists")
    else:
        os.mkdir(f"./{name}/")

def main():
    if not os.path.exists(f"./images_fresh"):
        os.mkdir(f"./images_fresh")

    dat = shelve.open("new3")
    threads = []
    for city, images in dat.items():
        thread = threading.Thread(target=download_images, args=(city, images))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
        
if __name__ == "__main__":
    main()