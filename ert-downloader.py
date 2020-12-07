from extractors import archive_extractor, ertflix_extractor, generic_extractor
from downloader import downloader
import sys

if __name__ == "__main__":
    url = sys.argv[1]
    if "archive.ert" in url:
        stream_data = archive_extractor.obtain_data(url)
    elif "webtv.ert" in url or "ertflix.gr" in url:
        stream_data = archive_extractor.obtain_data(url)
    else:
        stream_data = archive_extractor.obtain_data(url)

    downloader.download(stream_data)
