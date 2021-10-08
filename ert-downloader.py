from extractors import archive_extractor, ertflix_extractor
from downloaders import m3u8_downloader, alpha_downloader
import sys

if __name__ == "__main__":
    url = sys.argv[1]

    if "ertflix.gr" in url:
        extractor = ertflix_extractor.ErtflixExtractor(url)
        stream_data = extractor.obtain_data()
        m3u8_downloader.Downloader(stream_data).download()
    elif "archive.ert.gr" in url:
        extractor = archive_extractor.ArchiveExtractor(url)
        stream_data = extractor.obtain_data()
        m3u8_downloader.Downloader(stream_data).download()
    elif "alphatv.gr":
        alpha_downloader.AlphaDownloader(url).download()

