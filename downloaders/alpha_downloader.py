import requests
import re
from bs4 import BeautifulSoup
import sys


class AlphaDownloader:
    def __init__(self, url):
        self.url = self.construct_main_url(url)
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.title = self.obtain_title()
        self.download_url = self.obtain_download_url()

    def construct_main_url(self, url):
        suffix = re.split("vid", url)[1]
        return "https://www.alphatv.gr/ajax/Isobar.AlphaTv.Components.PopUpVideo.PopUpVideo.PlayMedia/?" + suffix

    def obtain_title(self):
        main_title = self.soup.find("div", {"class": "seasonDetails"}).findChild().text
        main_title = re.sub(":|\/|\||\"", "-", main_title);
        episode = self.soup.find("h2").text
        return main_title + " - " + episode

    def obtain_download_url(self):
        video_main_container = self.soup.find("div", class_="videoMainContainer")
        return re.findall('https:[^"]*', video_main_container['data-plugin-player'])[0]

    def download(self):
        print(self.title)

        response = requests.get(self.download_url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))

        print("Total Size: {} Mb".format(total_size_in_bytes * 10**(-6)))

        block_size = 10**3
        downloaded = 0
        with open("{}.mp4".format(self.title), 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded += 1
                sys.stdout.write("\rDownloaded {}/{} Mb".format(downloaded*10**(-3), total_size_in_bytes*10**(-6)))
                sys.stdout.flush()
        file.close()