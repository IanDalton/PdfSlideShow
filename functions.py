from screeninfo import get_monitors,Monitor
from PIL import Image
import fitz
import os
def get_largest_screen():
    dmax:Monitor = Monitor(0,0,0,0,0,0)
    
    for m in get_monitors():
        if dmax.height_mm*dmax.width_mm <= m.height_mm*m.width_mm:
            dmax=m
                
    return dmax

def extract_images(dir):
    if not os.path.exists('images'):
        os.makedirs('images')

    pdf_file = fitz.open(dir)
    page:fitz.Page
    piz: fitz.Pixmap
    filelist = [ f for f in os.listdir('images') if f.endswith(".jpg") ]
    for f in filelist:
        os.remove(os.path.join('images', f))
    
    for i,page in enumerate(pdf_file):
        piz = page.get_pixmap(matrix=fitz.Identity,dpi=None,colorspace=fitz.csRGB,clip=None,alpha=False,annots=False)
        """ og_height,og_width = piz.height,piz.width
        zoom = 1
        mat = fitz.Matrix(zoom,zoom)
        piz = page.get_pixmap(matrix=mat,dpi=None,colorspace=fitz.csRGB,clip=None,alpha=False,annots=False)

        print(og_height,piz.height) """

        piz.save(f"images/{i}.jpg")



def generate_image_list(x:int,y:int,dir:str)->list:
    images = list()
    for i in range(y):
            images.append([])
            for _ in range(x):
                images[i].append([])
    sort = list()
    for i in range(y):
        sort.append([])
    for i,image in enumerate(os.listdir(dir)):
        sort[i%y].append(f'{dir}/{image}')
    for yi,db in enumerate(sort):
        for i, image in enumerate(db):
              images[yi][i%x].append(image)
    return images

if __name__ == "__main__":
    for i in get_monitors():
        print(i)
    print(get_largest_screen())
    extract_images('pdf.pdf')
