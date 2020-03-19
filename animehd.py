#!/usr/bin/python3

import requests
import sys
import click
import requests
import bs4
import re
import os
from urllib.parse import urlparse
import argparse
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
import time 



#configuration params

chunk_size=4096

resolution={'360':'360p-0','480':'480p-1','720':'720p-2'}
# destination_folder=

download_type={
    'list':1,
    'single':0
}


# id=z-movie-server contains list of all servers

headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}


def to_mb(given_byte):
    return given_byte//(1024*1024)
link = "https://r3---sn-woc7ln7y.googlevideo.com/videoplayback?expire=1584367131&ei=-2lvXsKwE5SV1gab-oH4CA&ip=154.72.91.222&id=76486bc55a682230&itag=22&source=picasa&begin=0&requiressl=yes&mh=Rl&mm=30&mn=sn-woc7ln7y&ms=nxu&mv=u&mvi=2&pl=23&sc=yes&susc=ph&app=fife&mime=video/mp4&cnr=14&dur=1240.642&lmt=1583858785890299&mt=1584359604&sparams=expire,ei,ip,id,itag,source,requiressl,susc,app,mime,cnr,dur,lmt&sig=ADKhkGMwRQIgDbnJl1I5LMgBN8tS0qG-1ARywjXm4b7Mcu261DrbjvQCIQCRkySw8bv-4r4tjH7lsPVowX7sz_imm1HlB9UO3EXJ2A==&lsparams=mh,mm,mn,ms,mv,mvi,pl,sc&lsig=ABSNjpQwRQIgNWrB4YW61Lsf6_u8oFM4_-JhPCsJxwRp4RA6vY175rMCIQCd3edGD1bt8XCl00uXP3d2mPIPDQG0eHciQMVODQhfkw=="
file_name = "download1.mp4"

def get_video_folder():
    return os.path.expanduser("~")+'/Videos/'

def get_download_link(html):
    # resp=send_request(url_to_download_page)
    div_tag=parse_html(html,'zmovie-info')
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


def start_chrome():
    chrome_options = Options() 
    chrome_options.add_argument("--headless") 
    return webdriver.Chrome(executable_path=os.getcwd()+'/chromedriver',chrome_options=chrome_options)

def chrome_get_download_link(browser,url):
    browser.get(url)
    # wait 4 secs
    time.sleep(4)
    return browser.find_element_by_css_selector(".auto-download").get_attribute("href")


def get_servers(html,resolution_key):
    ul_tag=parse_html(html,'z-movie-server')
    li_list=ul_tag.find_all('li')
    dict_of_servers={}
    for li in li_list:
        server_name=li['class'][0]
        links=li.find_all('a')
        dict_of_servers[server_name]=[f'{link["href"]}download/{resolution[resolution_key]}' for link in links]
    return dict_of_servers

def parse_html(html,id):
    soup = bs4.BeautifulSoup(html,'lxml')
    return soup.find_all(id=id)[0]

def send_request(url):
    return s.get(url,headers=headers)

def download(link,file_name):
    with open(get_video_folder()+file_name, "wb") as f:
            response = requests.get(link, stream=True,headers=headers)
            total_length = response.headers.get('content-length')
            if total_length: # no content length header
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=chunk_size):
                    dl += len(data)
                    f.write(data)   
                    print(f'{to_mb(dl)} of {to_mb(total_length)}')
                    sys.stdout.flush()


if __name__ == "__main__":
    # sample_url="https://animehd47.com/naruto-dub/s1-m1/"
    s = requests.Session() 
    # resp=s.get(sample_url,headers=headers)
    # web_queue=[]
    # with open('Naruto (Dub) - Animehd47.com.html') as f:
    #     resp=f.read()
    # dict_of_servers=get_servers(resp,'720')
    # print(dict_of_servers)
            

    # send request to get the download link
    # resp=s.get(web_queue[0],headers=headers)
    # div_tag=parse_html(resp.text,'zmovie-info')
    # all_div_tag=div_tag.find_all('div')
    # download_link=all_div_tag[0].find_all('a',class_='btn btn-primary auto-download btn-lg')[0]['href']
    # print(download_link)
    # download(download_link)

    parser = argparse.ArgumentParser(description='Download Videos From Animehd.')
    parser.add_argument('url',help='url e.g https://animehd47.com/naruto-dub/s1-m1/')
    parser.add_argument('-r' ,default='720',choices=['360','480','720'])
    parser.add_argument('-d',default='ONE',choices=['ALL','ONE'])
    args=parser.parse_args()
    user_resolution=args.r
    user_download=args.d
    user_url=args.url

    # TODO: Validate the url, check if parser can do that

    # send request

    resp = send_request(user_url)
    if resp.status_code == requests.codes.ok:
        # start browser session here
        browser=start_chrome()
        dict_of_servers=get_servers(resp.text,user_resolution)
        # lets check what the user wants
        server_name,links_to_download=dict_of_servers.popitem()
        if user_download=='ALL':
            # download from the first server
            # TODO: if fail try the rest before giving up

            for link in links_to_download:
                result=send_request(link)
                if result.status_code == requests.codes.ok:
                    download_link=get_download_link(result.text)
                    download(download_link,generate_name(link,2))
        else:
            print('Downloading One file')
            result=send_request(links_to_download[0])
            if result.status_code==requests.codes.ok:
                print(links_to_download[0])
                download_link=chrome_get_download_link(browser,links_to_download[0])
                print(download_link)
                # download_link=get_download_link(result.text)
                download(download_link,generate_name(links_to_download[0],2))

            # download from the first server
            # TODO: if fail try the rest before giving up
    else:
        print('Http Error Code: '+resp.status_code)
    
    browser.close()





            


    