import os
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import pandas as pd
import requests

folder_path = "pages"

def excel_creater(directory, file_name, y, data):
    # Create a MultiIndex DataFrame
    sorted_years = sorted(y)
    columns = pd.MultiIndex.from_tuples(
        [(year, metric) for year in sorted_years for metric in ["TLR", "RPC", "GO", "OI", "Perception","City","State","Rank", "Score", "Link"]],
        names=["Year", "Metric"]
    )

    df_data = []
    for college, year_data in data.items():
        row = [college]
        for year in sorted_years:
            year_info = year_data.get(year, {"TLR": None, "RPC": None, "GO": None, "OI": None, "Perception": None, "City":None, "State": None, "Rank": None, "Score":None, "Link":None})
            row.extend([year_info["TLR"], year_info["RPC"], year_info["GO"], year_info["OI"], year_info["Perception"],year_info["City"],year_info["State"],year_info["Rank"], year_info["Score"], year_info["Link"]])
        df_data.append(row)

    df = pd.DataFrame(df_data, columns=pd.MultiIndex.from_product([["College"], [""]]).append(columns))
    with pd.ExcelWriter(os.path.join(directory,f"{file_name}.xlsx"), engine="openpyxl") as writer:
        df.to_excel(writer, index=True)

def create_category(directory, folder_name):
    folder_path = os.path.join(directory, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def scrap_data():
    for root, dirs, files in os.walk(folder_path):

        all_data = {}
        years = set()
        for file_name in files:
            # Get the full file path
            file_path = os.path.join(root, file_name)
            print(f"Processing file: {file_path}")


            info = re.search(r"\\([^\\]+)\\", file_path)
            create_category("data", info[1])

            pdf_path = os.path.join("data",info[1])

            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, "html.parser")

            rows = soup.find_all("tr")

            for row in rows:
                try:
                    name_td = row.find_all("td")
                    if len(name_td) < 4:
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


                    #Extracting city and state
                    city = name_td[-4].get_text(strip=True)
                    state = name_td[-3].get_text(strip=True)

                    # Extract Score using class "sorting_1"
                    rank_td = name_td[-1]
                    rank = rank_td.get_text(strip=True)

                    score_td = name_td[-2]
                    score = score_td.get_text(strip=True)

                    year = file_name.split('.')[0]
                    years.add(year)


                    pdf_link_tag = row.find("a", href=lambda x: x and x.endswith(".pdf"))
                    pdf_url = ""
                    if pdf_link_tag:
                        pdf_url = pdf_link_tag["href"]
                        pdf_url = urljoin("https://www.nirfindia.org", pdf_url)
                        name_td = row.find_all("td")
                        if len(name_td) < 2:
                            continue
                
                        college_name = name_td[1].get_text(strip=True).split("More Details")[0].strip()
                        create_category(pdf_path, college_name)

                        pdf_name = os.path.join(os.path.join(pdf_path, college_name), f"{year}.pdf")

                        response = requests.get(pdf_url)
                        if response.status_code == 200:
                            with open(pdf_name, "wb") as pdf_file:
                                pdf_file.write(response.content)
                            print(f"Downloaded: {year}.pdf")
                        else:
                            print(f"Failed to download: {year}.pdf ({pdf_url})")
                    

                    if college_name not in all_data:
                        all_data[college_name] = {}

                    all_data[college_name][year] = {
                            "TLR": tlr,
                            "RPC": rpc,
                            "GO": go,
                            "OI": oi,
                            "Perception": perception,
                            "City":city,
                            "State":state,
                            "Rank":rank,
                            "Score": score,
                            "Link":pdf_url,
                    }
                except Exception as e:
                    print(f"Error processing row in file {file_name}: {e}")
            
            excel_creater(os.path.join("data",info[1]),info[1],years,all_data)


print("Data extracted and saved to 'nirf_report.xlsx'")