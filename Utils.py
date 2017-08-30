import nltk
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import BytesIO as StringIO
import shutil

def copy_file_to_folder(filename, to_folder):
    shutil.copy(filename, to_folder)

def get_keywords(fpath):
    with open(fpath) as f:
        lines = f.read().splitlines()
    return lines

def pdf_to_text(pdfname):
    print (pdfname)

    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    fp = open(pdfname, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text.decode(codec)


# get resume tokens from text
def split_text_to_tokens(filename):

    raw_text = pdf_to_text(filename)
    special_characters = [",", ".", "'", ";", "\n", "\t"]

    def clean_text():
        cleaned_string = raw_text.lower()
        for string in special_characters:
            cleaned_string = cleaned_string.replace(string, " ")
        cleaned_string = cleaned_string.lower()
        return cleaned_string

    def tokenize():
        cleaned_text = clean_text()
        text_tokens = cleaned_text.split(" ")
        return [word for word in text_tokens if word != ""]

    tokens = tokenize()

    # no need to use nltk to get bigrams and trigrams though
    bigrams = [bigram[0] + ' ' + bigram[1] for bigram in nltk.bigrams(tokens)]
    trigrams = [trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] for trigram in nltk.trigrams(tokens)]
    return tokens + bigrams + trigrams