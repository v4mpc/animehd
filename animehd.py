#!/usr/bin/python3

import requests
import click
import os


# configuration params
chunk_size = 1024
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}
animes = [
    {
        'destination_path': "/home/v4mpc/Videos/boruto/",
        'name': 'boruto',
        'start_at': 1,
        'link': 'https://fb.manga47.net/Boruto_Dub/Boruto_Dub_00',
        'file_name': 'Boruto'

    },
    {
        'destination_path': "/home/v4mpc/Videos/one_piece/",
        'name': 'one_piece',
        'start_at': 90,
        'link': 'https://op.manga47.net/One_Piece_Dub/0',
        'file_name': 'One_piece'

    }
]


class AnimeNotFoundError(Exception):
    pass


def video_exists(destination_path, file_name, link):
    # cretera for existance
    # file_name and file_size match
    file_list = os.listdir(destination_path)
    if file_name in file_list:
        return os.path.getsize(destination_path+file_name)
    return 0


def get_anime(name):
    for anime in animes:
        # print(anime['name'])
        if anime['name'] == name:
            # print('am herer')
            return anime
    raise AnimeNotFoundError


def partial_download(destination_path, file_name, link):

    # resume_headers = {'Range':'bytes=0-2000000'}
    start_at = video_exists(destination_path, file_name, link)
    headers['Range'] = f'bytes={start_at}-'
    response = requests.get(link, stream=True, headers=headers)
    partial_length = response.headers.get('content-length')
    if partial_length:  # no content length header
        total_length = int(response.headers['Content-Range'].split('/')[1])
        with click.progressbar(length=total_length,
                               label=file_name) as bar:
            with open(destination_path+file_name, "ab") as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    dl = len(data)+start_at
                    f.write(data)
                    bar.update(dl)
                    start_at = 0
            return


@click.command()
@click.argument('name')
def main(name):
    try:
        anime = get_anime(name)
        start_at = anime['start_at']
        while start_at < 100:
            # TODO: implement 001...010...100 in start_at for link and file_name
            file_name = f"{anime['file_name']}_0{start_at}.mp4"
            link = f"{anime['link']}{start_at}.MP4"
            destination_path = anime['destination_path']
            partial_download(destination_path, file_name, link)
            start_at += 1
    except AnimeNotFoundError:
        click.echo(f"Anime {name} not configured")


if __name__ == "__main__":
    main()
