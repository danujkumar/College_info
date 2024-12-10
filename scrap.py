# Creating the api so that realtime data can be fetched from it

from data.scrap_pdf import scrap_pdf
from data.scrape_data import scrap_data

# Scraping the website
scrap_data()

# Scraping the pdfs
scrap_pdf()