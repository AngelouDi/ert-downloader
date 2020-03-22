import requests
import os
from multiprocessing.pool import ThreadPool
import re
import sys

if __name__ == "__main__":

    url_root = ''
    url = ''
    text = ''
    files = []
    page_url = sys.argv[1]  # website url
    threads = 5  # amount of workers who are downloading at the same time

    page = (requests.get(page_url).text.split('\n'))  # getting the source code of the page

    title = re.split('/', page_url)[-2]  # get the title of the video (it's the last segment of the url, I'm lazy)

    for i in page:
        if '.mp4' in i:  # finds the url in the source code of the video that contains the
            url = i      # link for the stream link (.mp4) that contains the .m3u8 files
            break
    video_url = re.split('src="|&', url)[1]  # extract the forementioned link
    video_file = requests.get(video_url).text.split('\n')  # reading the 'video file' that contains the necessary link

    for i in video_file:  # getting the .mp4 link
        if '.mp4' in i:
            url_root = (i.split("'")[1].split('.mp4')[0]+'.mp4/')  # find the link we will use to get the .m3u8 link
            if("ep.ert.gr/" in url_root):
                break

    playlist_m3u8 = requests.get(url_root+'playlist.m3u8', verify=False).text  # this file contains
    # the link for the file that contains the links of each video segment
    try:  # fixing geolocation issue for some videos
        chunklist_url = playlist_m3u8.split('\n')[3]
        playlist_m3u8 = requests.get(url_root + 'playlist.m3u8', verify=False).text
    except:
        url_root = url_root.replace('dvrorigin/', 'dvrorigingr/')
        playlist_m3u8 = requests.get(url_root + 'playlist.m3u8', verify=False).text
        chunklist_url = playlist_m3u8.split('\n')[3]

    chunklist_m3u8 = requests.get(url_root + chunklist_url, verify=False).text  # we generate it and get the file
    chunklist_lines = chunklist_m3u8.split('\n')

    for i in chunklist_lines:
        if '.ts' in i:  # we get each segment filename that's used to generate the urls of each
            files.append(i)
            text += 'file ' + i + '\n'

    w = open('filenames.txt', 'w+')  # the file with the filenames for the ffmpeg
    w.write(text)
    w.close()

    def download(link):
        with open(link, 'wb') as f:
            file = requests.get(url_root+link, verify=False)
            f.write(file.content)

    pool = ThreadPool(threads)  # multithreading to download many segments simultaniously
    thread = pool.map(download, files)
    pool.close()
    pool.join()  # waiting for the downloads to complete

    os.system(('ffmpeg -f concat -i filenames.txt -acodec copy -vcodec copy {0}.mp4').format(title))   # finally we can
    # GENERATE THE VIDEO

    for i in files:
        os.remove(i)  # delete the segments we downloaded, unless you wanna run out of storage, it's up to you <3
