from io import StringIO, BytesIO
from urllib import *
import requests
from numpy import *
from pandas import *
from PyPDF2 import PdfReader

filename = "2024FD_Alex.txt"
docID = []
urls = []

with open(filename) as file:
    lines = file.readlines()
    line_count = len(lines)

count = 0
for i in lines:
    parts = lines[count].split()
    docID.append(parts[-1])

    url = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/" + str(docID[count]) + ".pdf"
    urls.append(url)
    count += 1

for url in urls:
   try:
       response = requests.get(url)
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       print(f"Error fetching PDF from {url}: {e}")
       continue

   pdf_file = BytesIO(response.content)
   pdf_reader = PdfReader(pdf_file)

   all_page_text = ""
   for page_num in range(len(pdf_reader.pages)):
       page = pdf_reader.pages[page_num]
       page_text = page.extract_text()
       all_page_text += page_text

   print(f"Text from {url}:\n{all_page_text}")
