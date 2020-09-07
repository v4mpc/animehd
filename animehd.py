#!/usr/bin/python3

import requests
import click
import requests
import os
import time


# configuration params

chunk_size = 1024

resolution = {'360': '360p-0', '480': '480p-1', '720': '720p-2'}
# destination_folder=

download_type = {
    'list': 1,
    'single': 0
}


destination_path = "/home/v4mpc/Videos/one_piece/"


# id=z-movie-server contains list of all servers

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}


def video_exists(destination_path, file_name, link):
    # cretera for existance
    # file_name and file_size match
    file_list = os.listdir(destination_path)
    if file_name in file_list:
        # check size
        response = requests.head(link, headers=headers)
        # remote_size = response.headers.get('content-length')
        # local_size =
        # return int(local_size) >= int(remote_size)
        return os.path.getsize(destination_path+file_name)
    return 0


def download(link, file_name):
    with open(destination_path+file_name, "wb") as f:
        response = requests.get(link, stream=True, headers=headers)
        total_length = response.headers.get('content-length')
        if total_length:  # no content length header
            total_length = int(total_length)
            with click.progressbar(length=total_length,
                                   label=file_name) as bar:
                for data in response.iter_content(chunk_size=chunk_size):
                    dl = len(data)
                    f.write(data)
                    bar.update(dl)


def partial_download():
    file_name = f'One_Piece_03.mp4'
    link = 'https://op.manga47.net/One_Piece_Dub/03.MP4'
    # response = requests.head(link, headers=headers)
    # remote_size = response.headers.get('content-length')
    # local_size = os.path.getsize(destination_path+file_name)
    # print()
    # print(remote_size)
    # exit()
    # resume_headers = {'Range':'bytes=0-2000000'}
    with open(destination_path+file_name, "ab") as f:
        start_at = video_exists(destination_path, file_name, link)
        headers['Range'] = f'bytes={start_at}-'
        # with open(destination_path+file_name, "ab") as f:

        response = requests.get(link, stream=True, headers=headers)
        # print()
        # exit()
        partial_length = response.headers.get('content-length')
        if partial_length:  # no content length header
            total_length = int(response.headers['Content-Range'].split('/')[1])
            with click.progressbar(length=total_length,
                                   label=file_name) as bar:
                for data in response.iter_content(chunk_size=chunk_size):
                    dl = len(data)+start_at
                    # print(dl)
                    f.write(data)
                    bar.update(dl)
                    start_at = 0


if __name__ == "__main__":

    partial_download()
