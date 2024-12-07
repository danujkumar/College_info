import os
import requests
import re
from datetime import datetime

# List of URLs to scrape
urls_univ = [
    "https://www.nirfindia.org/Rankings/2017/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2019/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2018/UniversityRanking.html"
]

urls_engg = [
    "https://www.nirfindia.org/Rankings/2017/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2018/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2019/EngineeringRanking.html"
]

urls = {
    "University":urls_univ,
    "Engineering":urls_engg
}

url = [urls]

def create_category(directory, folder_name):
    folder_path = os.path.join(directory, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Processing each key-value pair
for url_dict in url:
    for key, value in url_dict.items():
        #Creating folder with name of key
        create_category("pages", key)
        create_category("data",key)
        for url in value:
            try:
                response = requests.get(url)
                response.raise_for_status()
                html_content = response.text

                # Generate a unique file name
                pattern = r"Rankings/(\d{4})"
                # Find all matches
                years = re.findall(pattern, url)

                #Saving the pages .html
                folder_path = os.path.join("pages", key)
                file_path = os.path.join(folder_path, years[0]+".html")
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(html_content)

                print(f"Saved: {file_path}")

            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch {url}: {e}")
