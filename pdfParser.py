from pypdf import *
from io import StringIO, BytesIO
from urllib import *
from requests import *

filename = "2024FD.txt"
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

writer = StringIO.PdfFileWriter()

for url in urls:
    remoteFile = StringIO.urlopen(Request(url)).read()
    memoryFile = StringIO(remoteFile)
    pdfFile = StringIO.PdfFileReader(memoryFile)

    for pageNum in xrange(pdfFile.getNumPages()):
            currentPage = pdfFile.getPage(pageNum)
            writer.addPage(currentPage)

    outputStream = open("output.pdf","wb")
    writer.write(outputStream)
    outputStream.close()