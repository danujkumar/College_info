import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import pandas as pd

folder_path = "pages"

all_data = {}
years = set()


for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        # Get the full file path
        file_path = os.path.join(root, file_name)
            
        # Process the file (you can replace this with your file processing logic)
        print(f"Processing file: {file_path}")

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
                
                year = file_name.split('.')[0]
                years.add(year)

                if college_name not in all_data:
                    all_data[college_name] = {}

                all_data[college_name][year] = {
                        "TLR": tlr,
                        "RPC": rpc,
                        "GO": go,
                        "OI": oi,
                        "Perception": perception,
                        "Link": pdf_url
                }
            except Exception as e:
                print(f"Error processing row in file {file_name}: {e}")

# Create a MultiIndex DataFrame
sorted_years = sorted(years)
columns = pd.MultiIndex.from_tuples(
    [(year, metric) for year in sorted_years for metric in ["TLR", "RPC", "GO", "OI", "Perception", "Link"]],
    names=["Year", "Metric"]
)

df_data = []
for college, year_data in all_data.items():
    row = [college]
    for year in sorted_years:
        year_info = year_data.get(year, {"TLR": None, "RPC": None, "GO": None, "OI": None, "Perception": None, "Link": None})
        row.extend([year_info["TLR"], year_info["RPC"], year_info["GO"], year_info["OI"], year_info["Perception"], year_info["Link"]])
    df_data.append(row)

df = pd.DataFrame(df_data, columns=pd.MultiIndex.from_product([["College"], [""]]).append(columns))
with pd.ExcelWriter("nirf_report.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, index=True)
excel_path = "nirf_report.xlsx"
print("Data extracted and saved to 'nirf_report.xlsx'")