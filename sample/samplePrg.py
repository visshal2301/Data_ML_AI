import requests
import csv

# Step 1: Call the API endpoint
url = "https://jsonplaceholder.typicode.com/posts"  # sample public API
response = requests.get(url)

# Step 2: Parse JSON output
if response.status_code == 200:
    data = response.json()
else:
    print("Failed to retrieve data:", response.status_code)
    data = []

# Step 3: Convert JSON to CSV
if data:
    # Extract keys from the first JSON object for CSV headers
    keys = data[0].keys()

    with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print("CSV file 'output.csv' created successfully!")
else:
    print("No data to write.")