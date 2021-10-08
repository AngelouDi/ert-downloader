import requests
import re
from bs4 import BeautifulSoup
import json


class ErtflixExtractor:
    def __init__(self, url):
        self.index_url = ""
        self.base_url = ""
        self.url = url
        self.html = requests.get(url).text
        self.title = self.obtain_title()
        self.obtain_title()
        self.id = self.obtain_id()
        self.details = self.get_details()
        self.codename = self.get_codename()
        self.index = self.obtain_index()
        self.chunklist = self.obtain_chunklist()

    def obtain_title(self):
        soup = BeautifulSoup(self.html, "html.parser")
        title = soup.find('title').text
        title = re.sub(":|/|\||\"", "-", title);
        print(title)
        return title

    def obtain_id(self):
        return re.findall("(?!.*\/)[^-]*", self.url)[0]

    def get_details(self):
        params = (
            ('platformCodename', 'www'),
            ('id', self.id),
            ('$headers', '{"X-Api-Date-Format":"iso","X-Api-Camel-Case":true}')
        )
        response = requests.get('https://api.app.ertflix.gr/v1/Tile/GetSeriesDetails', params=params)
        return json.loads(response.text)

    def select_episode(self):
        episode_list = []
        i = 0
        for season in self.details["episodeGroups"]:
            print("{}".format(season["title"]))
            for episode in season["episodes"]:
                episode_info = {}

                try:
                    episode_info["codename"] = episode["codename"]
                except KeyError:
                    raise
                for info in ["episodeNumber", "seasonNumber", "subtitle", "shortDescription"]:
                    try:
                        episode_info[info] = episode[info]
                    except KeyError:
                        episode_info[info] = ""

                episode_list.append(episode_info)
                print("\t[{}] {} - {} - {}".format(i, episode_list[-1]["episodeNumber"], episode_list[-1]["subtitle"], episode_list[-1]["shortDescription"]))
                i += 1

        selection = int(input("\nΔιαλέξτε Επεισόδιο | Select Episode\n"))
        selected_episode = episode_list[selection]
        self.title = "{} s{}e{} - {}".format(self.title, selected_episode["seasonNumber"], selected_episode["episodeNumber"], selected_episode["subtitle"])
        return selected_episode["codename"]

    def obtain_index(self):
        params = (
            ('platformCodename', 'www'),
            ('codename', self.codename)
        )

        response = requests.get('https://api.app.ertflix.gr/v1/Player/AcquireContent', params=params)
        data = json.loads(response.text)
        self.index_url = data["MediaFiles"][0]["Formats"][0]["Url"]

        return requests.get(self.index_url).text

    def select_resolution(self):
        index = self.index
        formats = re.findall("#EXT-X-STREAM-INF.*", index)
        links = re.findall("#EXT-X-STREAM-INF.*[\r\n]+([^\r\n]+)", index)

        i = 0
        for selection in formats:
            print("[{}] {}".format(i, selection))
            i += 1

        selection = input("Διαλέξτε επιθυμητή ανάλυση | Select wanted format\n")
        return links[int(selection)]

    def obtain_chunklist(self):
        self.base_url = re.findall(".*\/",self.index_url)[0]
        stream_suffix = self.select_resolution()
        chunkist_url = self.base_url + stream_suffix
        clean_chunklist = []
        chunklist = requests.get(chunkist_url).text.split('\n')
        for chunk in chunklist:
            if ".ts" in chunk:
                clean_chunklist.append(chunk)
        return clean_chunklist

    def get_codename(self):
        is_series = "ser" in self.id
        if is_series:
            return self.select_episode()
        else:
            return re.findall("-.*", self.url)[0][1:]

    def obtain_data(self):
        return {"title": self.title, "chunklist": self.chunklist, "base_url": self.base_url}


