import requests
import re

class MegatvExtractor:
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text
        self.title = self.obtain_title()
        self.index = self.obtain_index()
        self.base_url = re.split("playlist.m3u8", self.index)[0]
        self.chunklist = self.obtain_chunklist()

    def obtain_title(self):
        title = re.findall('document.title = "[^"]*', self.html)[0][18:]
        title = re.sub(":|/|\||\"", "-", title);
        print(title)
        return title

    def obtain_index(self):
        index = re.findall('data-kwik_source=".*m3u8', self.html)[0][18:]
        return index

    def select_resolution(self):
        index = requests.get(self.index).text
        formats = re.findall("#EXT-X-STREAM-INF.*", index)
        links = re.findall("#EXT-X-STREAM-INF.*[\r\n]+([^\r\n]+)", index)

        i = 0
        for selection in formats:
            print("[{}] {}".format(i, selection))
            i += 1

        selection = input("Διαλέξτε επιθυμητή ανάλυση | Select wanted format\n")
        return links[int(selection)]

    def obtain_chunklist(self):
        chunklist_suffix = self.select_resolution()
        chunklist_url = self.base_url + chunklist_suffix
        clean_chunklist = []
        chunklist = requests.get(chunklist_url).text.split('\n')
        for chunk in chunklist:
            if ".ts" in chunk:
                clean_chunklist.append(chunk)
        return clean_chunklist

    def obtain_data(self):
        return {"title": self.title, "chunklist": self.chunklist, "base_url": self.base_url}