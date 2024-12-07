import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

folder_path = "pages"
pdf_folder = "pdf_details"
os.makedirs(pdf_folder, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

def generate_unique_filename(base_name, folder):
    counter = 1
    unique_name = base_name
    while os.path.exists(os.path.join(folder, f"{unique_name}.pdf")):
        unique_name = f"{base_name} ({counter})"
        counter += 1
    return unique_name

for file_name in os.listdir(folder_path):
    if file_name.endswith(".html"):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")
        rows = soup.find_all("tr")

        for row in rows:
            try:
                pdf_link_tag = row.find("a", href=lambda x: x and x.endswith(".pdf"))
                if pdf_link_tag:
                    pdf_url = pdf_link_tag["href"]
                    pdf_url = urljoin("https://www.nirfindia.org", pdf_url)

                    name_td = row.find_all("td")
                    if len(name_td) < 2:
                        continue
                    college_name = name_td[1].get_text(strip=True).split("More Details")[0].strip()

                    safe_name = sanitize_filename(college_name)
                    unique_name = generate_unique_filename(safe_name, pdf_folder)
                    pdf_name = os.path.join(pdf_folder, f"{unique_name}.pdf")

                    response = requests.get(pdf_url)
                    if response.status_code == 200:
                        with open(pdf_name, "wb") as pdf_file:
                            pdf_file.write(response.content)
                        print(f"Downloaded: {unique_name}.pdf")
                    else:
                        print(f"Failed to download: {unique_name}.pdf ({pdf_url})")
            except Exception as e:
                print(f"Error processing row in file {file_name}: {e}")

print("PDF download completed!")
