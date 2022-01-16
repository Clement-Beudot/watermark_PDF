from PyPDF2 import PdfFileWriter, PdfFileReader
import os.path

INBOX = os.path.join("automatic", "inbox")
OUTBOX = os.path.join("automatic", "outbox")
SIGNATURE = "signature.pdf"


files_list = []

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


        # fichier_brut.close()
        watermark_file.close()
        input_file.close()
        output_file.close()





"""contenu_sortie = PdfFileWriter()

fichier_pdf_signature = open("signature.pdf", "rb")
fichier_pdf_recap = open("recap.pdf", "rb")

signature = PdfFileReader(fichier_pdf_signature)
reader_recap = PdfFileReader(fichier_pdf_recap)
page1_recap = reader_recap.getPage(0)
page1_recap.mergePage(signature.getPage(0))



contenu_sortie.addPage(page1_recap)
for i in range(1, reader_recap.getNumPages()):
    contenu_sortie.addPage(reader_recap.getPage(i))


fichier_sortie = open("fichier_sortie.pdf", "wb")
contenu_sortie.write(fichier_sortie)

fichier_sortie.close()
fichier_pdf_signature.close()
fichier_pdf_recap.close()"""