ert-downloader
==============

This tool is used to download videos from Greece's public national channel webtv, EΡΤ. At https://webtv.ert.gr'

Usage
=====

python ert-downloader.py [url]

If you are on linux, you probably have to change the ffmpeg line to "os.system(('./ffmpeg ...", so putting an './' in front of the 'ffmpeg'.

Example
=======

python ert-downloader.py https://webtv.ert.gr/ert1/sta-akra/27mar2019-sta-akra-theodosis-tasios/


Dependencies
============

This script relies on ffmpeg to encode the video. You can get it from the official source at https://ffmpeg.org/download.html 
