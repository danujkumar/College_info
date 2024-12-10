import os
import requests
import re
from datetime import datetime

# List of URLs to scrape
urls_univ = [
    "https://www.nirfindia.org/Rankings/2017/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2019/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2018/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2020/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2021/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2022/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2023/UniversityRanking.html",
    "https://www.nirfindia.org/Rankings/2024/UniversityRanking.html",
]

urls_engg = [
    "https://www.nirfindia.org/Rankings/2017/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2018/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2019/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2020/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2021/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2022/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2023/EngineeringRanking.html",
    "https://www.nirfindia.org/Rankings/2024/EngineeringRanking.html",
]

urls_mgmt = [
    "https://www.nirfindia.org/Rankings/2017/ManagementRanking.html",
    "https://www.nirfindia.org/Rankings/2018/ManagementRanking.html",
    "https://www.nirfindia.org/Rankings/2019/ManagementRanking.html",
    "https://www.nirfindia.org/Rankings/2020/ManagementRanking.html",
    "https://www.nirfindia.org/Rankings/2021/ManagementRanking.html",
    "https://www.nirfindia.org/Rankings/2022/ManagementRanking.html",
    "https://www.nirfindia.org/Rankings/2023/ManagementRanking.html",
    "https://www.nirfindia.org/Rankings/2024/ManagementRanking.html"
]

urls_coll = [
    "https://www.nirfindia.org/Rankings/2017/CollegeRanking.html",
    "https://www.nirfindia.org/Rankings/2018/CollegeRanking.html",
    "https://www.nirfindia.org/Rankings/2019/CollegeRanking.html",
    "https://www.nirfindia.org/Rankings/2020/CollegeRanking.html",
    "https://www.nirfindia.org/Rankings/2021/CollegeRanking.html",
    "https://www.nirfindia.org/Rankings/2022/CollegeRanking.html",
    "https://www.nirfindia.org/Rankings/2023/CollegeRanking.html",
    "https://www.nirfindia.org/Rankings/2024/CollegeRanking.html",
]

urls_pharm = [
    "https://www.nirfindia.org/Rankings/2017/PharmacyRanking.html",
    "https://www.nirfindia.org/Rankings/2018/PharmacyRanking.html",
    "https://www.nirfindia.org/Rankings/2019/PharmacyRanking.html",
    "https://www.nirfindia.org/Rankings/2020/PharmacyRanking.html",
    "https://www.nirfindia.org/Rankings/2021/PharmacyRanking.html",
    "https://www.nirfindia.org/Rankings/2022/PharmacyRanking.html",
    "https://www.nirfindia.org/Rankings/2023/PharmacyRanking.html",
    "https://www.nirfindia.org/Rankings/2024/PharmacyRanking.html"
]
urls_med = [
    "https://www.nirfindia.org/Rankings/2018/MEDICALRanking.html",
    "https://www.nirfindia.org/Rankings/2019/MEDICALRanking.html",
    "https://www.nirfindia.org/Rankings/2020/MEDICALRanking.html",
    "https://www.nirfindia.org/Rankings/2021/MEDICALRanking.html",
    "https://www.nirfindia.org/Rankings/2022/MEDICALRanking.html",
    "https://www.nirfindia.org/Rankings/2023/MEDICALRanking.html",
    "https://www.nirfindia.org/Rankings/2024/MEDICALRanking.html"
]

urls_arch = [
    "https://www.nirfindia.org/Rankings/2018/ArchitectureRanking.html",
    "https://www.nirfindia.org/Rankings/2019/ArchitectureRanking.html",
    "https://www.nirfindia.org/Rankings/2020/ArchitectureRanking.html",
    "https://www.nirfindia.org/Rankings/2021/ArchitectureRanking.html",
    "https://www.nirfindia.org/Rankings/2022/ArchitectureRanking.html",
    "https://www.nirfindia.org/Rankings/2023/ArchitectureRanking.html",
    "https://www.nirfindia.org/Rankings/2024/ArchitectureRanking.html",
]
urls_law = [
    "https://www.nirfindia.org/Rankings/2018/LAWRanking.html",
    "https://www.nirfindia.org/Rankings/2019/LAWRanking.html",
    "https://www.nirfindia.org/Rankings/2020/LAWRanking.html",
    "https://www.nirfindia.org/Rankings/2021/LAWRanking.html",
    "https://www.nirfindia.org/Rankings/2022/LAWRanking.html",
    "https://www.nirfindia.org/Rankings/2023/LAWRanking.html",
    "https://www.nirfindia.org/Rankings/2024/LAWRanking.html",
]

urls_den = [
    "https://www.nirfindia.org/Rankings/2020/DentalRanking.html",
    "https://www.nirfindia.org/Rankings/2021/DentalRanking.html",
    "https://www.nirfindia.org/Rankings/2022/DentalRanking.html",
    "https://www.nirfindia.org/Rankings/2023/DentalRanking.html",
    "https://www.nirfindia.org/Rankings/2024/DentalRanking.html",
]

urls_res = [
    "https://www.nirfindia.org/Rankings/2021/ResearchRanking.html",
    "https://www.nirfindia.org/Rankings/2022/ResearchRanking.html",
    "https://www.nirfindia.org/Rankings/2023/ResearchRanking.html",
    "https://www.nirfindia.org/Rankings/2024/ResearchRanking.html"
]

urls_agri = [
    "https://www.nirfindia.org/Rankings/2023/AgricultureRanking.html",
    "https://www.nirfindia.org/Rankings/2024/AgricultureRanking.html"
]

urls_inv = [
    "https://www.nirfindia.org/Rankings/2023/InnovationRanking.html",
    "https://www.nirfindia.org/Rankings/2024/InnovationRanking.html",
]

urls_open = [
    "https://www.nirfindia.org/Rankings/2024/OPENUNIVERSITYRanking.html"
]

urls_skill = [
    "https://www.nirfindia.org/Rankings/2024/SKILLUNIVERSITYRanking.html"
]

urls_state = [
    "https://www.nirfindia.org/Rankings/2024/STATEPUBLICUNIVERSITYRanking.html"
]
urls = {
    "University":urls_univ,
    "Engineering":urls_engg,
    "Management": urls_mgmt,
    "College":urls_coll,
    "Pharmacy" : urls_pharm,
    "Medical": urls_med,
    "Architecture" : urls_arch,
    "Law" : urls_law,
    "Dental" : urls_den,
    "Research":urls_res,
    "Agriculture" : urls_agri,
    "Innovation" : urls_inv,
    "Open" : urls_open,
    "Skill" : urls_skill,
    "State" : urls_state
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
