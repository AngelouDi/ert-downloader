import requests
import re


class StarExtractor:
    def __init__(self, url):
        self.url = url
        self.base_url = ""
        self.html = requests.get(url).text
        self.title = self.obtain_title()
        self.data_video = self.obtain_data_video()
        self.id = self.obtain_id()
        self.index = "https://cdnapisec.kaltura.com/p/713821/sp/0/playManifest/entryId/{}/format/applehttp/protocol/https/flavorParamId/0/manifest.m3u8".format(self.data_video)
        self.chunklist = self.obtain_chunklist()


    def obtain_title(self):
        title = re.findall('data-title=.[^"]*', self.html)[0][12:]
        title = re.sub(":|\/|\||\"", "-", title);
        print(title)
        return title

    def obtain_id(self): #useless
        id = re.findall('div id=.[^"]*', self.html)[0][8:]
        return id

    def obtain_data_video(self):
        data_video = re.findall('data-video=.[^"]*', self.html)[1][12:]
        return data_video

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
        chunklist = self.select_resolution()
        clean_chunklist = []
        chunklist = requests.get(chunklist).text.split('\n')
        for chunk in chunklist:
            if ".ts" in chunk:
                suffix = re.split("\/(?!.*\/)", chunk)[1]
                self.base_url = re.split("\/(?!.*\/)", chunk)[0] + "/"
                clean_chunklist.append(suffix)
        print(clean_chunklist)
        return clean_chunklist

    def obtain_data(self):
        return {"title": self.title, "chunklist": self.chunklist, "base_url": self.base_url}
