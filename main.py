from PyPDF2 import PdfFileWriter, PdfFileReader
import os.path

INBOX = ""
OUTBOX = ""
WATERMARK = ""

def set_config(): 
    global INBOX, OUTBOX, WATERMARK
    f = open("watermark.config", "w")
    INBOX = input("Manually enter the path to the INBOX folder, or drag and drop it : ")
    OUTBOX = input("Manually enter the path to the OUTBOX folder, or drag and drop it : ")
    WATERMARK = input("Manually enter the path to the Watermark.pdf file, or drag and drop it : ")
    settings = "INBOX:"+ INBOX.strip("'") + "\nOUTBOX:" + OUTBOX.strip("'") + "\nWATERMARK:" + WATERMARK.strip("'")
    f.write(settings)
    f.close()



def check_config(config_dict):
    for keys in config_dict:
        if not os.path.exists(config_dict[keys]):
            print("Error : \n", config_dict[keys], ": No such file or directory\n")
            return False
    return True


def get_config():
    if os.path.exists("watermark.config"):
        f = open("watermark.config", "r")
        config = f.readlines()        
        config_dict = {}
        for element in config:
            if element.split(":")[1][-4:] == ".pdf":
                config_dict[element.split(":")[0]] = element.split(":")[1]
            else: 
                config_dict[element.split(":")[0]] = element.split(":")[1][:-1]
        global INBOX, OUTBOX, WATERMARK
        try : 
            INBOX, OUTBOX, WATERMARK = config_dict["INBOX"], config_dict["OUTBOX"], config_dict["WATERMARK"]
            check_config(config_dict)
        except KeyError:
            print("ERROR : There is someting wrong with the config file \"watermark.config\"")
            if input("\nDo you want to refigure ? (Y)es / (S)top ").upper() == "Y" :
                set_config()
            else:
                exit(0) 
        f.close()      
    else:
        set_config()
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

get_config()
get_list()
print("You are about to edit", len(files_list), "file(s) : ")
for i in files_list:
    print("\t", i)

if input("\nConfirm ? (Y)es / (N)o ").upper() == "Y" :
    add_watermark()