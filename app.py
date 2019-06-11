import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

def getListOfQuotes():
    # load list of files in directory
    file_list = os.listdir('data')

    # remove files that don't start with digit
    for f in file_list:
        if not f[0].isdigit():
             file_list.remove(f)
    return file_list

def textExtractor(filename):
    f = open(filename, 'rb')

    parser = PDFParser(f)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''

    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()

    print(extracted_text)

    return extracted_text.split("\n")

def modelData(data):
    instance = {
        'customer': data[5],
        'customer_addr_1': data[6],
        'customer_addr_2': data[7],
        'customer_addr_3': data[8],
        'customer_po': data[11],
        'quote_date': data[14],
        'quote_number': data[16],
        'nass_po': data[18]
    }

    return instance


def main():
    datadir = 'data/'
    raw_data = []
    data = []

    quotes_list = getListOfQuotes()
    for q in quotes_list:
        raw_data.append(textExtractor(datadir + q))

    for d in raw_data:
        data.append(modelData(d))

    print(data)

if __name__ == '__main__':
    main()
