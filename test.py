
from PIL import Image
import fitz

pdf_file = fitz.open('I:/Github/PdfSlideShow/pdf.pdf')


page:fitz.Page
piz: fitz.Pixmap
for i,page in enumerate(pdf_file):
    piz = page.get_pixmap(matrix=fitz.Identity,dpi=None,colorspace=fitz.csRGB,clip=None,alpha=False,annots=False)
    og_height,og_width = piz.height,piz.width
    zoom = 0.56
    mat = fitz.Matrix(zoom,zoom)
    piz = page.get_pixmap(matrix=mat,dpi=None,colorspace=fitz.csRGB,clip=None,alpha=False,annots=False)

    print(og_height,piz.height)

    piz.save(f"ca{i}.jpg")





    