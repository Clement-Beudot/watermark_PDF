from PyPDF2 import PdfFileWriter, PdfFileReader
import os.path

INBOX = os.path.join("automatic", "inbox")
OUTBOX = os.path.join("automatic", "outbox")
SIGNATURE = "signature.pdf"


def add_watermark():
    for path, subdirs, files in os.walk(INBOX):
        for name in files:
            name_str = "sign_" + name
            out_content = PdfFileWriter()
            watermark_file , input_file = open(SIGNATURE, "rb"), open(os.path.join(INBOX, name), "rb")
            watermark, input = PdfFileReader(watermark_file), PdfFileReader(input_file)
            page1 = input.getPage(0)
            page1.mergePage(watermark.getPage(0))
        
            out_content.addPage(page1)
            for i in range(1, input.getNumPages()):
                out_content.addPage(input.getPage(i))

            output_file = open(os.path.join(OUTBOX, name_str), "wb")
            out_content.write(output_file)

            watermark_file.close()
            input_file.close()
            output_file.close()

def get_list():
    for path, subdirs, files in os.walk(INBOX):
        for name in files:
            files_list.append(name)



files_list = []
get_list()
print("You are about to edit", len(files_list), "file(s) : ")
for i in files_list:
    print("\t", i)

if input("\nConfirm ? (Y)es / (N)o ").upper() == "Y" :
    add_watermark()