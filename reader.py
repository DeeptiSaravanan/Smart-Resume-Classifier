import PyPDF2
import docx
import string
import logging

logging.basicConfig(level=logging.DEBUG)

def fetch_pdf_page(file_name):

  # try:
    links = []
    file_pointer = open(file_name,'rb')

    # Setting up pdf document

    pdf_pages =PyPDF2.PdfFileReader(file_pointer)
    print(type(pdf_pages))
    num_pages=pdf_pages.getNumPages()

    #fetches URLs

    for pageno in range(0,num_pages):
      page=pdf_pages.getPage(pageno)
      page_data=page.extractText()
      print(type(page_data))
      print(page_data)

      # if 'Annots' in page.attrs.keys():
      #   link_object_list = page.attrs['Annots']
        # Due to implementation of pdfminer the link_object_list can either
        # be the list directly or a PDF Object reference
            # if type(link_object_list) is not list:
        # link_object_list = link_object_list.resolve()

    #     for link_object in link_object_list:
    #       if type(link_object) is not dict:
    #         link_object = link_object.resolve()
    #       if link_object['A']['URI']:
    #         links.append(link_object['A']['URI'])

    # file_pointer.close()
    # return links
  # except (Exception, exception_instance):
  #   logging.error('Error while fetching URLs : '+str(exception_instance))

    return ''

#Extract text from PDF

def getPDFContent(path):
        content = ""


    # Load PDF into pyPDF

    pdf = PyPDF2.PdfFileReader(open(path, "rb"))

    # Iterate pages

    for i in range(0, pdf.getNumPages()):

        # Extract text from page and add to content

        content += pdf.getPage(i).extractText() + "\n"

    # Collapse whitespace

    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

#Extract text from DOCX

def getText(filename):
    doc = docx.Document(filename)
        fullText = ""

    for para in doc.paragraphs:
        fullText += para.text
    return fullText

#To store extracted resumes

resume = ""

#Select a path to the file - code needs os.path #to be addded

filename = input("Enter file name / path : ")

#Invoking document parsers based on file format

#Note: for TXT - do a normal f.read()




