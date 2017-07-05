from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests


def download_page(link, song_name):
    '''
        Takes the final download page link and song name
        and searches for download link of song and downloads it
        in the current directory
    '''
    # get the source code of the download_page
    # final_page = requests.get(link)
    # print("got request")
    # final_plain_code = final_page.text
    # soup_obj_final = BeautifulSoup(final_plain_code, "lxml")
    # print("Got soup object")
    # # set the download_url to song download url
    # download_url = "http://www.youtubeinmp3.com" + soup_obj_final.find('a', {'id': 'download'})['href']
    # download song
    print("Downloading Song")
    urlretrieve(link, song_name + ".mp3")
    print("Downloaded!!")


def song_page(link, song_name):
    '''
        takes the song page link and song name
        then searches for final download page link
        and pass it to download_page function
    '''
    # get the source code of the songs page on utomp3.com
    next_page = requests.get(link)
    plain_code = next_page.text
    soup_obj = BeautifulSoup(plain_code, "lxml")
    # get the final download page link from the source code of the current song page
    link_to_final_page = soup_obj.find('a', {'rel': 'nofollow'})
    # print(link_to_final_page)
    print("Going to download page")
    download_page(link_to_final_page['href'], song_name)


def search_page(song_download):
    '''
        Searches for the song
        and calls song_page with proper link to the song
    '''
    link_song = ''
    # convert song name to url searchable form
    for words in song_download.split(' '):
        link_song = link_song + words + "+"
    url = "http://u2mp3.com/download.php?q=" + link_song[:-1].lower()
    # get the url source code
    request_obj = requests.get(url)
    plain_code = request_obj.text
    soup_obj = BeautifulSoup(plain_code, "lxml")
    # get the tag with the name of the song see source code of page
    for links in soup_obj.findAll('h4'):
        # skip to next link if current link is audio or instrumental
        if 'instrumental' not in links and 'audio' not in links:
            # get the next link
            next_link = links.findNext('a')['href']
            # print(next_link)
            print("Found your song")
            song_page(next_link, song_download)
            break


def main():
    fr = open("songs_to_download.txt", "r")
    fw = open("downloaded.txt", "a+")
    for song_name in fr.readlines():
        print("Song name : " + song_name.lower().title())
        search_page(song_name[:-1].lower().title())
        fw.write(song_name)

    fr.close()
    fw.close()
    # song_name = input()
    # search_page(song_name)

if __name__ == '__main__':
    main()
