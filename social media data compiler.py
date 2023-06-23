import json
import csv
import os

# Input the directory commands here
# directory = location of JSON files

# Get all JSON files from the directory
# Assumes all files relevant to the analysis are JSON file

json_files = [file for file in os.listdir(directory) if file.endswith('.json')]

social_media_data = []

# Loop through the files
for file in json_files:
    with open(os.path.join(directory, file), 'r') as json_file:
        json_data = json.load(json_file)
        # Determine the data type
        # Will update according to the conditions distinguishing the specific json files
        data_type = 'player' if 'player' in json_data else 'team'

        data_frame = [
            json_data['name'],
            json_data['followers'],
            json_data['following'],
            json_data['posts'],
            json_data['likes'],
            json_data['comments'],
            json_data['verified'],
            data_type
        ]
        social_media_data.append(data_frame)

# Write the data to CSV file

with open('social_media_data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['name', 'followers', 'following', 'posts', 'likes', 'comments', 'verified', 'type'])
    writer.writerows(social_media_data)


