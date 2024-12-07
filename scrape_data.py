import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd

folder_path = "pages"

all_data = []

for file_name in os.listdir(folder_path):
    if file_name.endswith(".html"):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        rows = soup.find_all("tr")

        for row in rows:
            try:
                name_td = row.find_all("td")
                if len(name_td) < 2:
                    continue
                college_name = name_td[1].get_text(strip=True).split("More Details")[0].strip()

                score_table = row.find("div", class_="tbl_hidden")
                if not score_table:
                    continue

                scores = score_table.find_all("td")

                if len(scores) < 5:
                    continue
                tlr = scores[0].text.strip()
                rpc = scores[1].text.strip()
                go = scores[2].text.strip()
                oi = scores[3].text.strip()
                perception = scores[4].text.strip()

                pdf_link_tag = row.find("a", href=lambda x: x and x.endswith(".pdf"))
                pdf_url = ""
                if pdf_link_tag:
                    pdf_url = pdf_link_tag["href"]
                    pdf_url = urljoin("https://www.nirfindia.org", pdf_url)
                    

                all_data.append({
                    "College": college_name,
                    "TLR": tlr,
                    "RPC": rpc,
                    "GO": go,
                    "OI": oi,
                    "Perception": perception,
                    "Link" : pdf_url
                })
            except Exception as e:
                print(f"Error processing row in file {file_name}: {e}")

df = pd.DataFrame(all_data)
df.to_excel("nirf_report.xlsx", index=False)

#Saving the 

print("Data extracted and saved to 'nirf_report.xlsx'")
