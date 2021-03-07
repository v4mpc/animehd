import requests
import click
import os
import concurrent.futures
import time
import logging

import multiprocessing

print(multiprocessing.cpu_count())

logging.basicConfig(filename='thread.log', level=logging.INFO)

chunk_size = 1024
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}
animes = [
    {
        'destination_path': "/home/v4mpc/Videos/boruto/",
        'name': 'boruto',
        'start_at': 70,
        'link': 'https://fb.manga47.net/Boruto_Dub/Boruto_Dub_',
        'file_name': 'Boruto',
        'format': 'mp4'

    },
    {
        'destination_path': "/home/v4mpc/Videos/one_piece/",
        'name': 'one_piece',
        'start_at': 266,
        'link': 'https://on.manga47.net/One_Piece_Dub/',
        # https://on.manga47.net/One_Piece_Dub/267.mp4
        'file_name': 'One_Piece',
        'format': 'mp4'
    },
    {
        'destination_path': "/home/v4mpc/Videos/black_clover/",
        'name': 'black_clover',
        'start_at': 144,
        'link': 'https://fb.manga47.net/Black_Clover_TV_Sub/Black_Clover_TV_Sub_',
        'file_name': 'Black_Clover',
        'format': 'mp4'
    },
    {
        'destination_path': "/home/v4mpc/Videos/jujustu_kaisen/",
        'name': 'jujustu_kaisen',
        'start_at': 2,
        'link': 'https://20.manga47.net/Jujutsu_Kaisen_TV/Jujutsu_Kaisen_TV_',
        'file_name': 'Jujustu_Kaisen',
        'format': 'mp4'
    },
    {
        'destination_path': "/home/v4mpc/Videos/doctor_stone/",
        'name': 'doctor_stone',
        'start_at': 1,
        'link': 'https://20.manga47.net/Dr_Stone_Stone_Wars/Dr_Stone_Stone_Wars_Dub_',
        'file_name': 'Doctor_Stone',
        'format': 'mp4'
    }
]


def partial_download(file_name, start_at, end_at):

    # resume_headers = {'Range':'bytes=0-2000000'}

    # start_at = 0
    # end_at = 5000000
    # file_name = 'test.mp4'

    link = 'https://20.manga47.net/Dr_Stone_Stone_Wars/Dr_Stone_Stone_Wars_Dub_001.mp4'
    destination_path = '/home/v4mpc/repo/animehd/test/'
    start_at = video_exists(destination_path, file_name, link)
    headers['Range'] = f'bytes={start_at}-{end_at}'
    response = requests.get(link, stream=True, headers=headers)
    if response.status_code >= 400:
        print(response.status_code)
        return

    partial_length = response.headers.get('content-length')
    print(partial_length)
    if partial_length:  # no content length header
        # total_length = int(response.headers['Content-Range'].split('/')[1])
        print(f'Total length {to_mb(partial_length)} MB')
        dl = 0

        with open(destination_path+file_name, "ab") as f:

            for data in response.iter_content(chunk_size=chunk_size):
                print(len(data))
                dl = len(data)+dl
                print(f'Received {to_mb(dl)} MB of {to_mb(partial_length)} MB')
                f.write(data)
                # bar.update(dl)
                # start_at = 0
        return 1


def manager():
    number_of_worker = 8
    file_size = 111824365
    chunk_size, remaining_size = divmod(file_size, number_of_worker)
    # if not remaining_size:
    #     number_of_worker = 7

    videos = []
    for index in range(1, number_of_worker+1):
        start_itr = chunk_size*(index-1)
        end_itr = chunk_size*index
        videos.append(
            {'start': start_itr,
             'end': end_itr,
             'file_name': f'part{index}.mp4'
             }
        )
        if index == 1:
            break

    print(videos)
    return videos


def to_mb(bys):
    return int(bys)//1024**2


def video_exists(destination_path, file_name, link):
    # criteria for existance
    # file_name and file_size match
    file_list = os.listdir(destination_path)
    if file_name in file_list:
        return os.path.getsize(destination_path+file_name)
    return 0


if __name__ == "__main__":
    # manager(323)
    # main()
    # partial_download(0, 100)
    start_time = time.time()
    # videos = [
    #     {'start': 0,
    #      'end': 5000000,
    #      'file_name': 'part1.mp4'
    #      },
    #     {'start': 5000000,
    #      'end': 10000000,
    #      'file_name': 'part2.mp4'
    #      }
    # ]

    videos = manager()
    workers = []

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for video in videos:
    #         workers.append(executor.submit(
    #             partial_download, file_name=video['file_name'], start_at=video['start'], end_at=video['end']))
    #     # for future in concurrent.futures.as_completed(workers):
    #     #     print(future.result())

    #
    partial_download(videos[0]['file_name'], videos[0]
                     ['start'], videos[0]['end'])
    end_time = time.time()
    logging.info(f'Time used:{end_time-start_time}')
