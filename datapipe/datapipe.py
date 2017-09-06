import multiprocessing as mp
import concurrent.futures as cf
from google.cloud import storage
from . import scraper_google
from PIL import Image
import io
import requests
import os
import uuid
import time
import tarfile

def add_images(link_list, scrape, classname, site):
    try:
        print('Scraping', site,'for', classname)
        return scrape(classname)
    except Exception as e:
        print('Error with:', site, 'and class:', classname)
        print('Here\'s the error:', e)




def download(dname, fname, url):
    size = (1024,1024)
    try:
        image_content = requests.get(url, timeout=5).content

    except requests.exceptions.ConnectionError:
        print('ConnectionError, sleeping then trying again.')
        time.sleep(5)
        image_content = requests.get(url, timeout=5).content

    except requests.exceptions.InvalidSchema:
        # image is probably base64 encoded
        image_data = re.sub('^data:image/.+;base64,', '', url)
        image_content = base64.b64decode(image_data)

    except Exception as e:
        print('could not read', e, url)
        return False

    image_file = io.BytesIO(image_content)

    try:
        image = Image.open(image_file).convert('RGB')
        resized = image.resize(size, Image.LANCZOS)
        with open(dname+'/'+fname+'.jpg', 'wb') as f:
            resized.save(f, 'JPEG', quality=100)
    except Exception as e:
        print('could not read', e, url)
        return False
    return True



def download_helper(arglist):

    for args in arglist:

        (i, num_links, link, classname) = args
        print(i, '/', num_links)
        fname = str(uuid.uuid4())
        if not os.path.exists(classname):
            os.makedirs(classname, exist_ok=True)
        try:
            download(classname, fname, link)
        except:
            print('Exception, didn\'t download!')
    return True





def new_process(email, classname):
    print('In a new process! Yay!')
    print('Class to search:', classname)
    print('Email to return to:', email)
    print('Current directory:', os.getcwd())
    
    link_list = []
    link_list.extend(add_images(link_list, scraper_google.scrape, classname, 'google'))
    print('Got this many URLs:', len(link_list))
    
    
    executor = cf.ThreadPoolExecutor(max_workers=100)
    arglist = []
    num_links = len(link_list)
    for i, link in enumerate(link_list):
        arglist.append((i, num_links, link, classname))
    num_images = len(arglist)
    num_thread = 100
    im_per_thread = int(num_images / num_thread)
    print('This many images per thread:', im_per_thread)
    futures = []
    for k in range(num_thread):
        start = k*im_per_thread
        end = (k+1)*im_per_thread
        future = executor.submit(download_helper, arglist[start:end])
        futures.append(future)

    for future in cf.as_completed(futures):
        print('Thread finished.')

    print('Done downloading the images.')
    
    tar =  tarfile.open(classname+'.tar.gz', 'w:gz')
    tar.add(classname)
    tar.close()
    
    
    
    
    client = storage.Client(project='project-4-177215')
        
    try:
        bucket = client.get_bucket('yzleafimages')
        print('Found the bucket.')
        blob = storage.Blob(classname+'.tar.gz', bucket)
        blob.upload_from_filename(classname+'.tar.gz')
        print('Successfully uploaded.')
        blob.make_public(client)
        url = blob.public_url
        print('Here\'s the generated URL:', url)

    except google.cloud.exceptions.NotFound:
        print('Sorry, that bucket does not exist!')






def start_job(email, classname):
    # Fork off a new process. Make sure this returns quickly.
    mp.Process(target=new_process, args=(email, classname)).start()
	
