from tkinter import Frame,PhotoImage,RAISED,Label,Tk


import fitz

pdf_file = fitz.open('I:/Github/PdfSlideShow/pdf.pdf')



for i,page in enumerate(pdf_file):
    piz = page.get_pixmap(matrix=fitz.Identity,dpi=None,colorspace=fitz.csRGB,clip=None,alpha=False,annots=False)
    piz.save(f"ca{i}.jpg")

    

    