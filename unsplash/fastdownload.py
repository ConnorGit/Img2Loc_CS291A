from concurrent.futures import ThreadPoolExecutor
import requests
import os
import time
import random
import pandas as pd

session = requests.Session()


def download_image(image_url, image_path):
    try:
        response = session.get(image_url, stream=True)
        response.raise_for_status()
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download {image_url}: {e}")


def download_images_concurrently(sampled_df, output_dir, url_column, id_column, delay=0.1):
    os.makedirs(output_dir, exist_ok=True)

    # Adjust the number of threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        for index, row in sampled_df.iterrows():
            image_url = row[url_column]
            photo_id = row[id_column]
            if pd.isna(image_url) or pd.isna(photo_id):
                raise Exception(
                    csv_file + ": row lacks url or id\n" + str(row))
            image_name = f"{index}-{photo_id}.jpg"
            image_path = os.path.join(output_dir, image_name)
            executor.submit(download_image, image_url, image_path)
            time.sleep(delay)


csv_files = [
    {"file": "nov_dec_2023.csv", "dir": "nov_dec_2023_photos"},
    {"file": "nov_dec_2019.csv", "dir": "nov_dec_2019_photos"}
]
url_column = "photo_image_url"
id_column = "photo_id"
num_photos = 1000
seed = 42

# Download images
for csv in csv_files:
    df = pd.read_csv(csv["file"])
    random.seed(seed)
    sampled_df = df.sample(n=num_photos, random_state=seed)
    download_images_concurrently(sampled_df, csv["dir"], url_column, id_column)
