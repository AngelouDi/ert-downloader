from multiprocessing.pool import ThreadPool
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import re
import os
import shutil
from pathvalidate import sanitize_filename

def download_process(link):
    if not os.path.exists('download_parts'):
        os.makedirs('download_parts')
    filename = re.split("/", link)[-1]
    with open("download_parts/" + filename, 'wb') as f:
        file = requests.get(link, verify=False)
        print("DOWNLOADING FILE {}". format(link))
        f.write(file.content)
    f.close()

def clean_junk():
    shutil.rmtree("download_parts")

class Downloader():
    def __init__(self, data):
        self.title = data["title"]
        self.base_url = data["base_url"]
        self.chunklist = data["chunklist"]
        self.download_list = self.generate_download_list()
        self.create_parts_txt()


    def generate_download_list(self):
        download_list = []
        for chunk in self.chunklist:
            download_list.append(self.base_url + chunk)
        return download_list

    def create_parts_txt(self):
        if not os.path.exists('download_parts'):
            os.makedirs('download_parts')
        with open("download_parts/parts", 'w+') as file:
            for chunk in self.chunklist:
                file.write("file {}\n".format(chunk))
        file.close()

    def download(self):
        # stream_url = stream_data["stream_url"]
        # base_url = stream_data["base_url"]
        # chunklist = stream_data["chunklist"]
        # create_parts_txt(chunklist)
        print("DOWNLOADING:{}".format(self.title))
        pool = ThreadPool(5)
        pool.map(download_process, self.download_list)
        pool.close()
        pool.join()  # waiting for the downloads to complete
        os.system(('ffmpeg -f concat -safe 0 -i download_parts/parts -acodec copy -vcodec copy "{}//{}.mp4"'.format(os.getcwd(), sanitize_filename(self.title))))
        clean_junk()



