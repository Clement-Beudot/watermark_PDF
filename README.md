### README.md

Required : PyPDF2 :

- `pip install PyPDF2`


This script allows you to take all the PDFs in a folder and add a watermark (signature, logo) to the first page of each document.
For the moment, you have to manually configure the path of the input folder, the output folder, and the path of the watermark file (in .pdf)

Example (if the inbox path folder is /home/yourname/my_pdf/inbox )

INBOX = os.path.join("home", "yourname", "my_pdf", "inbox")
