#!/home/v4mpc/.local/share/virtualenvs/animehd-QGHCqRyK/bin/python3

import requests
import click
import os
import json


# configuration params
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
        'start_at': 140,
        'link': 'https://op.manga47.net/One_Piece_Dub/',
        'file_name': 'One_Piece',
        'format': 'MP4'
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
    }
]


class AnimeNotFoundError(Exception):
    pass


def load_config():
    with open('config.json') as json_file:
        config = json.load(json_file)


def video_exists(destination_path, file_name, link):
    # criteria for existance
    # file_name and file_size match
    file_list = os.listdir(destination_path)
    if file_name in file_list:
        return os.path.getsize(destination_path+file_name)
    return 0


def get_anime(name):
    for anime in animes:
        if anime['name'] == name:
            return anime
    raise AnimeNotFoundError


def convert_to_three_digits(number_string):
    while len(number_string) != 3:
        number_string = "0"+number_string
    return number_string


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
        while start_at < 400:
            file_name = f"{anime['file_name']}_0{start_at}.mp4"
            link_counter = convert_to_three_digits(str(start_at))
            link = f"{anime['link']}{link_counter}.{anime['format']}"
            print(link)
            destination_path = anime['destination_path']
            partial_download(destination_path, file_name, link)
            start_at += 1
    except AnimeNotFoundError:
        click.echo(f"Anime {name} not configured")

        # https://fb.manga47.net/Boruto_Dub/Boruto_Dub_053.mp4


if __name__ == "__main__":
    main()
