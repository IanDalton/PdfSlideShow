from screeninfo import get_monitors,Monitor
from PIL import Image
import fitz
import os
import requests
import shutil
from datetime import  datetime
from multiprocessing import Process

def update():
    current_version = 'v0.0.3'
    # Set the repository URL and the current version of the script
    repo_url = 'https://api.github.com/repos/IanDalton/PdfSlideShow/releases/latest'
    
    
    # Get the latest release information from GitHub
    response = requests.get(repo_url)
    data = response.json()
    print('Calls remaining: ', response.headers['X-RateLimit-Remaining'])
    try:
        latest_version = data['tag_name']

        # Compare the current and latest versions
        if current_version != latest_version:
            print(f'New version available: {latest_version}')
            print('Updating...')

            # Download and extract the latest version of the code
            download_url = data['assets'][0]["browser_download_url"]
            response = requests.get(download_url, stream=True)
            with open('../update.zip', 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            shutil.unpack_archive('../update.zip','../')
            
            # Overwrite the local copy of the code with the latest version
            repo_name = 'PdfSlideShow'
        
        # Construct path to PdfSlideShow directory
            pdfslideshow_path = os.path.dirname(__file__)
            shutil.rmtree(pdfslideshow_path)
            shutil.move(f"../{repo_name}-{latest_version[1:]}/files", pdfslideshow_path)
            shutil.rmtree('../update.zip')
            shutil.rmtree(f"../{repo_name}-{latest_version[1:]}")
            
            print('Update complete!')

        else:
            print('No updates available.')
    except KeyError as e:
        print(e)
        if int(response.headers.get('X-RateLimit-Remaining')) == 0:
            print('Warning! No more calls this hour. Time until next update:', datetime.fromtimestamp(int(response.headers['X-RateLimit-Reset']))-datetime.now())
        pass

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
    
    filelist = [ f for f in os.listdir('images') if f.endswith(".jpg") ]
    for f in filelist:
        os.remove(os.path.join('images', f))

    processes = []
    for i,page in enumerate(pdf_file):
        p = Process(target=save_image, args=(dir,i))
        p.start()
        processes.append(p)
    p:Process
    for p in processes:
        p.join()

def save_image(pdf_dir,i):
    pdf_file = fitz.open(pdf_dir)
    page = pdf_file[i]
    piz = page.get_pixmap(matrix=fitz.Identity,dpi=500,colorspace=fitz.csRGB,clip=None,alpha=False,annots=False)
    piz.save(f"images/{i}.jpg")

def del_images(img_folder:str='images'):
    if os.path.exists(img_folder):
        shutil.rmtree(img_folder)

def generate_image_list(x:int,y:int,dir:str,video_folder:str=None)->list:
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
    if video_folder:
        for i,video in enumerate(os.listdir(video_folder)):
            sort[i%y].append(f'{video_folder}/{video}')
    for yi,db in enumerate(sort):
        for i, image in enumerate(db):
              images[yi][i%x].append(image)
    return images

if __name__ == "__main__":
    for i in get_monitors():
        print(i)
    print(get_largest_screen())
    extract_images('pdf.pdf')
