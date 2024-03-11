from io import StringIO, BytesIO
import urllib
import requests
import numpy as np
import pandas as pd
from PyPDF2 import PdfReader
from multiprocessing import Pool, freeze_support
import re

# Extracts text from the pdf using PyPDF2
def pdfExtractor(url):
   try:
       response = requests.get(url)
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       print(f"Error fetching PDF from {url}: {e}")
       return None

   pdf_file = BytesIO(response.content)
   pdf_reader = PdfReader(pdf_file)

   all_page_text = ""
   for page_num in range(len(pdf_reader.pages)):
       page = pdf_reader.pages[page_num]
       page_text = page.extract_text()
       all_page_text += page_text

   return all_page_text

# Main method declared so that multithread doesn't open threads recursively
def main():
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

    return urls

urls = main()

# Runs pdfExtractor with multiple threads to improve runtime
def multithread():   
    pdfData = []

    if __name__ == '__main__':
        freeze_support()

        with Pool() as pool:
            results = pool.map(pdfExtractor, urls)

        for url, text in zip(urls, results):
            if text:
                pdfData.append(text)
            else:
                print(f"Failed to extract text from {url}")

    return pdfData

# Initializes unparsed data to the result of multithread method 
unparsedData = multithread()

# Initializes dictionary with columns needed
parsedData = {
    "Name" : [],
    "Date" : [],
    "Report Date" : [],
    "Symbol": [],
    "Amount": []
}

# TODO: Data to gather:
# - Politician name (Complete)
# - Date 
# - Report date
# - Stock symbol
# - Amount (Partially complete)

# Iterates through each item in the unparsed data
for item in unparsedData:
    lines = item.splitlines()
    amtFound = False

    # Iterates through each line in each item, processes name but only first amount
    # TODO: Process date ranges & multiple transactions per report
    for line in lines:

        if line.startswith("Name:"):
            currName = line.split(":")[1].strip()
            parsedData["Name"].append(currName)

        if "$" in line and not amtFound:
            # Uses re library to find date ranges within a line, since location of date range varies
            match = re.search(r"\$\d+(?:,\d{3})*(?:\.\d+)?", line)
            if match and (match.group() != "$200"):
                # print(match)
                parsedData["Amount"].append(match.group())
                amtFound = True

print(parsedData)

# df = pd.DataFrame(parsedData)