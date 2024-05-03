from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import get_countries_capital_population
from tqdm import tqdm

import requests
import io
import os, time
import shelve
import pandas as pd
import threading
from PIL import Image

def create_folder(name):
    if os.path.exists(f"./{name}"):
        print("Folder already exists")
    else:
        os.mkdir(f"./{name}")


def get_images_from_google(wd, url, delay, max, currlist):

    start = time.time()
    wd.implicitly_wait(delay)

    def scroll_down(wd):
        #A javascript script to scroll
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    
    #Loads the page
    wd.get(url)

    try:
        accept = wd.find_element(By.CSS_SELECTOR, ".sy4vM")
        wd.execute_script("arguments[0].click();", accept)
    except Exception as e:
        print("Probably no need")

    #Keep going till you get enuf images
    image_url = set()
    scroll_down(wd)
    time.sleep(delay)
    scroll_down(wd)
    time.sleep(delay)
    scroll_down(wd)
    scroll_down(wd)
    time.sleep(delay)
    scroll_down(wd)
    time.sleep(delay)
    scroll_down(wd)
    scroll_down(wd)
    time.sleep(delay)
    scroll_down(wd)
    time.sleep(delay)
    scroll_down(wd)
    scroll_down(wd)
    time.sleep(delay)
    scroll_down(wd)
    time.sleep(delay)
    scroll_down(wd)

    # We need to find the class names which all images share
    # This is YQ4gaf, might be different for others
    thumbnails = wd.find_elements(By.CSS_SELECTOR, ".tile--img__img")
    #Removing images that are not proper.
    for img in thumbnails[::]:
        if "zr758c" in img.get_attribute("class") or "wA1Bge" in img.get_attribute("class"):
            thumbnails.remove(img)
    # We don't wanna loop through images we already added or more than max
    for img in tqdm(thumbnails, desc = 'Progress'):
        try:
            wd.execute_script("arguments[0].click();", img)
        except Exception as e:
            print("Just continue", e)
            continue
        # We wanna click the bigger image now which has class sFlh5c pT0Scc iPVvYb
        image = wd.find_element(By.CLASS_NAME, "detail__media__img-highres")
        #if we are clicking on the same image just skip it
        # I had to hard code this to search inside shelve
        if image.get_attribute('src') in image_url or image.get_attribute('src') in currlist:
            continue
        else:
            if image.get_attribute('src') and "http" in image.get_attribute('src'):
                image_url.add(image.get_attribute('src'))

        if len(image_url) >= max: break

    end = time.time()
    print(f"{len(image_url)} images scraped in {(end - start)/60} minutes")
    return list(image_url)

def google_search_query(query):
    return f"https://www.google.com/search?tbm=isch&q={query}"

def duck_search_query(query):
    return f"https://duckduckgo.com/?q={query}&iax=images&ia=images"

def scrape_city_url(city, prompt_index, wd, c):
    match prompt_index:
        case 0: 
            images = get_images_from_google(wd, duck_search_query(f"{city} city aerial view"), 0.5, 125, c)
        case 1:
            images = get_images_from_google(wd, duck_search_query(f"city aerial view {city}"), 0.5, 125, c)
        case 2:
            images = get_images_from_google(wd, duck_search_query(f"{city} aerial view scenery"), 0.5, 125, c)
        case _:
            images = get_images_from_google(wd, duck_search_query(f"eye view {city}"), 0.5, 125, c)
    return images

def scrape_city_urls(dest, countries):
    country_city_dict = get_countries_capital_population()
    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Activate headless mode

    # Initialize WebDriver with Chrome options
    wd = webdriver.Chrome(options=chrome_options)
    for country in countries:
        city = country_city_dict[country]
        urls = shelve.open(dest)    
        if city not in urls or len(urls[city]) < 190:
            print(f"{city} not scraped...")
            try:
                current_urls = []
                for i in range(4):
                    c = [] if city not in urls else list(urls[city])
                    current_urls = current_urls + scrape_city_url(city, i, wd, c)
                    urls[city] = current_urls
                    print("Now scraped prompt", i + 1)
                urls[city] = current_urls
                urls.close()    
            except Exception as e:
                print(f"Error occurred while scraping {city}: {e}")
                continue
            print(f"{city} has been scraped")
        else:
            print(f"{city} already scraped")
    #Closes webdriver
    wd.quit()

def main():
    countries = ['Russia', 'Japan', 'United Arab Emirates',
                'United States', 'Mexico', 'Canada', 
                'Italy', 'France', 'United Kingdom',
                'Brazil', 'Argentina', 'Peru',
                'Kenya', 'Egypt', 'Morocco',                
                'Australia', 'New Zealand', 'Philippines']
    scrape_city_urls('new3', countries)

if __name__ == "__main__":
    main()