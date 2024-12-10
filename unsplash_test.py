import os
import random
import pandas as pd
import numpy as np
from img2loc_GPT4V import GPT4v2Loc
import re
from tqdm import tqdm

from geopy.distance import geodesic
from apikey import API_KEY

folder_path = "nov_dec_2023_photos"
random.seed(42)
total = len(os.listdir(folder_path))
num_photos = 500
start_index = 0
#Change start index to 500 to test the rest
file_list = random.sample(sorted(os.listdir(folder_path)), total)[start_index:start_index+num_photos]
np.save("Analyzed_list" + "_" + folder_path, file_list)

df = pd.read_csv("nov_dec_2023.csv")

use_database_search = True
num_nearest_neighbors = 8
num_farthest_neighbors = 8
skipped = 0
total = 0

pattern = r"(-?\d+\.?\d*),\s*(-?\d+\.?\d*)"

accuracies = np.zeros(5)

for file in tqdm(file_list, desc="Processing"):
    index = int(file[:file.find('-')])
    lat = df.iloc[index]['photo_location_latitude']
    long = df.iloc[index]['photo_location_longitude']
    true = (lat, long)
    
    image_path = folder_path + '/' + file
    GPT_Agent = GPT4v2Loc(device="cpu")

    GPT_Agent.set_image(image_path, use_database_search = use_database_search, num_neighbors = num_nearest_neighbors, num_farthest = num_farthest_neighbors)

    response = GPT_Agent.get_location(API_KEY, use_database_search)
    try:
        matches = re.search(pattern, response).group()
        #Originally lat_str, lon_str, but GPT is consistently giving lon first for some reason
        lon_str, lat_str = matches.split(',')
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
    except:
        skipped += 1
accuracies /= total
print(str(total) + " out of " + str(num_photos) + " successfully analyzed.")
print(accuracies)
    
np.save(folder_path + '_accuracies_' + str(total) + '_of_' + str(num_photos), accuracies)




