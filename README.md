Steps to reproduce our results:

Download the MP16 dataset from https://huggingface.co/datasets/Jia-py/MP16-Pro/tree/main

Build the clip embeddings and Faiss index with https://github.com/rom1504/clip-retrieval/tree/main 

Download test dataset and metadata, http://www.mediafire.com/file/7ht7sn78q27o9we/im2gps3ktest.zip, https://raw.githubusercontent.com/TIBHannover/GeoEstimation/original_tf/meta/im2gps3k_places365.csv

Install necessary dependencies

Run replication_test.py

Request access to unsplash full dataset, and get the photos.tsv000 file

Run unsplash/fastdownload.py and unsplash/builddataset.py

Run unsplash_test.py, switch files to 2019, run unsplash_test.py again

Change GPT_Agent.get_location to GPT_Agent.get_location_new in replication test.py and run again to test new prompt

Run multi_test.py to test prompt with neighbor images included
