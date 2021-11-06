import requests
import re
from bs4 import BeautifulSoup


class ArchiveExtractor:
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text
        self.title = self.obtain_title()
        self.base_url = self.obtain_base_url()
        self.chunklist = self.obtain_chunklist()

    def obtain_title(self):
        soup = BeautifulSoup(self.html, "html.parser")
        title = soup.find('title').text
        title = re.sub(":|\/|\||\"", "-", title);
        print(title)
        return title

    def obtain_base_url(self):
        soup = BeautifulSoup(self.html, "html.parser")
        player_iframe = soup.find('iframe')
        player_url = re.split('&', (player_iframe.attrs["src"]))[0]

        response = requests.get(player_url)
        url = re.findall("var HLSLink = '(.*)'", response.text)[0]
        base_url = re.findall(".*\/", url)[0]
        return base_url


    def obtain_chunklist(self):
        chunkist_url = self.base_url + "chunklist.m3u8"
        clean_chunklist = []
        chunklist = requests.get(chunkist_url).text.split('\n')
        for chunk in chunklist:
            if ".ts" in chunk:
                clean_chunklist.append(chunk)
        return clean_chunklist

    def obtain_data(self):
        return {"title": self.title, "chunklist": self.chunklist, "base_url": self.base_url}