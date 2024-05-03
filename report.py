import shelve
import pandas as pd
import os
import sys
# The urls are stored in the shelve file

# This script reports the number of urls stored as well as number of duplicates

def report1(special_interest = []):
    urls = shelve.open("new1")


    for city in urls:
        images = urls[city]
        seen = set()
        before = len(images)
        for image in images:
            seen.add(image)
        print(f"For {city}, {before} urls, {before - len(seen)} duplicates")
        if city in special_interest:
            print(images)

    print(f"Currently, {len(urls.keys())} / 35 scraped")

def report2():
    dat = shelve.open("new3")
    total_count = 0
    downloaded_count = 0
    for city, images in dat.items():
        image_total = 0
        image_downloaded = 0
        for i, image in enumerate(images):
            total_count += 1
            image_total += 1
            extensions = ['jpeg', 'jpg', 'png', 'gif', 'webp']  # Add more extensions if needed
            for ext in extensions:
                if os.path.exists(f"./images_fresh/{city}/{city}{i+1}.{ext}"):
                    downloaded_count += 1
                    image_downloaded += 1
                    break  # If any of the extensions is found, consider the image as downloaded
        print(f"{city}: {image_downloaded} / {image_total} of scraped is downloaded")
    print("Total:")
    print(f"{downloaded_count} / {total_count} of scraped is downloaded")
    count = 0
    for city, images in dat.items():
        if os.path.exists(f"./images_fresh/{city}"):
            count += 1
    print(f"{count} / {18} of countries is downloaded")
  
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py [report_number]")
        print("report_number: 1 or 2")
        return

    report_number = int(sys.argv[1])

    if report_number == 1:
        report1()
    elif report_number == 2:
        report2()
    else:
        print("Invalid report number. Please choose 1 or 2.")

if __name__ == "__main__":
    main()