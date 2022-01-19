from PyPDF2 import PdfFileWriter, PdfFileReader
import os.path

INBOX = "rien inbox" #os.path.join("automatic", "inbox")
OUTBOX = "rien outbox" #os.path.join("automatic", "outbox")
WATERMARK = "rien signature" #"signature.pdf"


def get_config():
    if os.path.exists("watermark.config"):
        f = open("watermark.config", "r")
        config = f.readlines()
        
        config_dict = {}
        for element in config:
            config_dict[element.split(":")[0]] = element.split(":")[1][:-1]
        global INBOX, OUTBOX, WATERMARK
        try : 
            INBOX, OUTBOX, WATERMARK = config_dict["INBOX"], config_dict["OUTBOX"], config_dict["WATERMARK"]
            if "" in config_dict.values():
                print("ERROR : There is someting wrong with the config file \"watermark.config\"")
                print("At least one argument has no value.")
                exit(0)
        except KeyError:
            print("ERROR : There is someting wrong with the config file \"watermark.config\"")
            if input("\nDo you want to refigure ? (Y)es / (S)top ").upper() == "Y" :
                print("reconfiguration")
            else:
                exit(0)

        
    else:
        f = open("watermark.config", "w")
    return config_dict



def add_watermark():
    for path, subdirs, files in os.walk(INBOX):
        for name in files:
            name_str = "sign_" + name
            out_content = PdfFileWriter()
            watermark_file , input_file = open(WATERMARK, "rb"), open(os.path.join(INBOX, name), "rb")
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
test = get_config()
print(INBOX)
print(OUTBOX)
print(WATERMARK)

get_list()
print("You are about to edit", len(files_list), "file(s) : ")
for i in files_list:
    print("\t", i)

if input("\nConfirm ? (Y)es / (N)o ").upper() == "Y" :
    add_watermark()