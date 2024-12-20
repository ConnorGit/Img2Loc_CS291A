import os
import random
import pandas as pd
import numpy as np
from img2loc_GPT4V import GPT4v2Loc
import re
from tqdm import tqdm

from geopy.distance import geodesic
from apikey import API_KEY

folder_path = "im2gps3ktest"
random.seed(42)
total = len(os.listdir(folder_path))
num_photos = 300
start_index = 0
#Change start index to 500 to test the rest
file_list = random.sample(sorted(os.listdir(folder_path)), total)[start_index:start_index+num_photos]
np.save("Analyzed_list" + "_" + folder_path, file_list)

df = pd.read_csv("im2gps3k_places365.csv")

use_database_search = True
num_nearest_neighbors = 8
num_farthest_neighbors = 8
skipped = 0
total = 0
i = 0

pattern = r"(-?\d+\.?\d*),\s*(-?\d+\.?\d*)"

accuracies = np.zeros(5)

for file in tqdm(file_list, desc="Processing"):
    i += 1
    metadata = df[df["IMG_ID"] == file]
    lat = metadata["LAT"].values[0]
    long = metadata["LON"].values[0]
    true = (lat, long)
    
    image_path = folder_path + '/' + file
    GPT_Agent = GPT4v2Loc(device="cpu")

    GPT_Agent.set_image(image_path, use_database_search = use_database_search, num_neighbors = num_nearest_neighbors, num_farthest = num_farthest_neighbors)

    response = GPT_Agent.get_location(API_KEY, use_database_search)
    try:
        matches = re.findall(pattern, response)[-1]
        lat_str, lon_str = matches
        latitude = float(lat_str)
        longitude = float(lon_str)
        guess = (latitude, longitude)

        distance = geodesic(guess, true).kilometers

        if(distance <= 1): accuracies += 1
        elif(distance <= 25): accuracies[1:] += 1
        elif(distance <= 200): accuracies[2:] += 1
        elif(distance <= 750): accuracies[3:] += 1
        elif(distance <= 2500): accuracies[4] += 1

        total += 1
        if(total % 10 == 0): np.save(folder_path + '_newprompt_accuracies_' + str(total) + '_of_' + str(i), accuracies / total)

    except:
        skipped += 1



accuracies /= total
print(str(total) + " out of " + str(num_photos) + " successfully analyzed.")
print(accuracies)
    
#np.save(folder_path + '_accuracies_' + str(total) + '_of_' + str(num_photos), accuracies)
np.save(folder_path + '_newprompt_accuracies_' + str(total) + '_of_' + str(num_photos), accuracies)





