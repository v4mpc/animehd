#!/usr/bin/python3

import requests
import sys
import click
import requests
import bs4
import re
import os
from urllib.parse import urlparse



#configuration params

chunk_size=4096

resolution_list=['360p-0','480p-1','720p-2']
# destination_folder=

download_type={
    'list':1,
    'single':0
}


# id=z-movie-server contains list of all servers

headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}


def to_mb(byte):
    return byte//(1024*1024)
link = "https://r3---sn-woc7ln7y.googlevideo.com/videoplayback?expire=1584367131&ei=-2lvXsKwE5SV1gab-oH4CA&ip=154.72.91.222&id=76486bc55a682230&itag=22&source=picasa&begin=0&requiressl=yes&mh=Rl&mm=30&mn=sn-woc7ln7y&ms=nxu&mv=u&mvi=2&pl=23&sc=yes&susc=ph&app=fife&mime=video/mp4&cnr=14&dur=1240.642&lmt=1583858785890299&mt=1584359604&sparams=expire,ei,ip,id,itag,source,requiressl,susc,app,mime,cnr,dur,lmt&sig=ADKhkGMwRQIgDbnJl1I5LMgBN8tS0qG-1ARywjXm4b7Mcu261DrbjvQCIQCRkySw8bv-4r4tjH7lsPVowX7sz_imm1HlB9UO3EXJ2A==&lsparams=mh,mm,mn,ms,mv,mvi,pl,sc&lsig=ABSNjpQwRQIgNWrB4YW61Lsf6_u8oFM4_-JhPCsJxwRp4RA6vY175rMCIQCd3edGD1bt8XCl00uXP3d2mPIPDQG0eHciQMVODQhfkw=="
file_name = "download1.mp4"

def get_video_folder():
    return os.path.expanduser("~")+'/Videos/'

def get_download_link(url_to_download_page):
    resp=send_request(url_to_download_page)
    div_tag=parse_html(resp.text,'zmovie-info')
    all_div_tag=div_tag.find_all('div')
    return all_div_tag[0].find_all('a',class_='btn btn-primary auto-download btn-lg')[0]['href']

def generate_name(url,name_type):
    #1=>folder, 2=>file
    o=urlparse(url)
    return o.path.split("/")[name_type]

def check_exist(user_path):
    return os.path.exists(user_path)

def create_dir(dir_name):
    return os.mkdir(get_video_folder+dir_name)



def parse_html(html,id):
    soup = bs4.BeautifulSoup(html,'lxml')
    return soup.find_all(id=id)[0]

def send_request(url):
    return s.get(url,headers=headers)

def download(link):
    with open(file_name, "wb") as f:
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')

            if total_length: # no content length header
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=chunk_size):
                    dl += len(data)
                    f.write(data)
                    # sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )   
                    print(f'{to_mb(dl)} of {to_mb(total_length)}')
                    sys.stdout.flush()

if __name__ == "__main__":
    # sample_url="https://animehd47.com/naruto-dub/s1-m1/"
    s = requests.Session() 
    # resp=s.get(sample_url,headers=headers)
    web_queue=[]
    with open('Naruto (Dub) - Animehd47.com.html') as f:
        resp=f.read()
        # print(resp)
    ul_tag=parse_html(resp,'z-movie-server')
    li_list=ul_tag.find_all('li')
    for li in li_list:
        links=li.find_all('a')
        for link in links:
            href=f'{link["href"]}/download/{resolution_list[1]}'
            web_queue.append(href)
            # print(f'{link["href"]}/download/{resolution_list[1]}')

    # send request to get the download link
    resp=s.get(web_queue[0],headers=headers)
    div_tag=parse_html(resp.text,'zmovie-info')
    all_div_tag=div_tag.find_all('div')
    download_link=all_div_tag[0].find_all('a',class_='btn btn-primary auto-download btn-lg')[0]['href']
    print(download_link)
    download(download_link)

    # p

    # print(web_queue)
            


    