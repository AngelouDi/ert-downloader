from multiprocessing.pool import ThreadPool
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import re
import os
import shutil

def generate_download_list(url, chunklist):
    download_list = []
    for chunk in chunklist:
        download_list.append(url + '/' + chunk)
    return download_list

def download_process(link):
    if not os.path.exists('download_parts'):
        os.makedirs('download_parts')
    filename = re.split("/", link)[-1]
    with open("download_parts/" + filename, 'wb') as f:
        file = requests.get(link, verify=False)
        print("DOWNLOADING FILE {}". format(link))
        f.write(file.content)
    f.close()

def create_parts_txt(chunklist):
    if not os.path.exists('download_parts'):
        os.makedirs('download_parts')
    with open("download_parts/parts", 'w+') as file:
        for chunk in chunklist:
            file.write("file {}\n".format(chunk))
    file.close()

def clean_junk():
    shutil.rmtree("download_parts")

def download(stream_data):
    stream_url = stream_data["stream_url"]
    chunklist = stream_data["chunklist"]
    create_parts_txt(chunklist)
    title = stream_data["title"]
    print("DOWNLOADING:{}".format(title))
    download_list = generate_download_list(stream_url, chunklist)
    pool = ThreadPool(5)
    pool.map(download_process, download_list)
    pool.close()
    pool.join()  # waiting for the downloads to complete
    os.system(('ffmpeg -f concat -i download_parts/parts -acodec copy -vcodec copy "{}.mp4"'.format(title)))
    clean_junk()



