import pandas as pd

file_path = "photos.tsv000"

# Reading a TSV file
df = pd.read_csv(file_path, sep="\t")

# Filter rows where the specified columns are not null
df = df.dropna(subset=["ai_primary_landmark_name",
                       "photo_location_latitude", "photo_location_longitude"])


# Ensure latitude and longitude are not (0, 0)
df = df[(abs(df["photo_location_latitude"]) > 0.001) |
        (abs(df["photo_location_longitude"]) > 0.001)]

# Convert 'photo_submitted_at' column to datetime
df["photo_submitted_at"] = pd.to_datetime(
    df["photo_submitted_at"], errors="coerce")

# Filter for November and December 2023
nov_dec_2023 = df[
    (df["photo_submitted_at"].dt.year == 2023) &
    (df["photo_submitted_at"].dt.month.isin([11, 12]))
]

# Filter for November and December 2019
nov_dec_2019 = df[
    (df["photo_submitted_at"].dt.year == 2019) &
    (df["photo_submitted_at"].dt.month.isin([11, 12]))
]

# Debugging: Display the first 5 rows of each bucket
columns_to_display = ["photo_location_latitude", "photo_location_longitude"]

print("November and December 2023 Data:")
print(nov_dec_2023[columns_to_display].head(5))

print("\nNovember and December 2019 Data:")
print(nov_dec_2019[columns_to_display].head(5))

# Output the November and December 2023 data to a CSV file
nov_dec_2023.to_csv("nov_dec_2023.csv", index=False)

# Output the November and December 2019 data to a CSV file
nov_dec_2019.to_csv("nov_dec_2019.csv", index=False)
