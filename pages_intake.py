import os
import requests
from datetime import datetime

# List of URLs to scrape
urls = [
    "https://www.nirfindia.org/Home/univ",
    "https://www.nirfindia.org/Home/engg",  
    "https://www.nirfindia.org/Home/mgmt",
    "https://www.nirfindia.org/Home/pharma",
    "https://www.nirfindia.org/Rankings/2017/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2017/ManagementRanking.html",
    "https://www.nirfindia.org/Rankings/2017/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2017/CollegeRanking.html",
    "https://www.nirfindia.org/Rankings/2017/PharmacyRanking.html",
]

# Folder to save HTML files
folder_name = "pages"
os.makedirs(folder_name, exist_ok=True)

# Function to generate a unique file name
def generate_file_name(base_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Timestamp for uniqueness
    return f"{base_name}_{timestamp}.html"

# Save each page
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Generate a unique file name
        base_name = url.split("/")[-1] or "index"  # Use last part of URL as base name
        file_name = generate_file_name(base_name)
        file_path = os.path.join(folder_name, file_name)

        # Save the HTML content
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"Saved: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
