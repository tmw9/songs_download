from bs4 import BeautifulSoup
import requests
# from urllib.request import urlretrieve
import shutil


def download_song(link, song_name):
    '''
        downloads the song
    '''
    # print(link)
    print("Downloading Now")
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        with open(song_name + '.mp3', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    print("Downloaded\n")


def song_page(link, song_name):
    '''
        goes to the song download page and passes the download link to download function
    '''
    request_obj = requests.get(link)
    plain_code = request_obj.text
    soup_obj = BeautifulSoup(plain_code, "lxml")
    # print(soup_obj)
    download_link = soup_obj.find('a', {'id': 'dn'})
    # print(soup_obj.findAll('a'))
    print("Found Download Link")
    # if download_link is None:
    #     download_link = download_link1
    try:
        download_song(download_link['href'], song_name)
    except Exception as e:
        print("Error : " + str(e))
        print("Cannot Download " + song_name + " because the song was removed")
        return


def search_song(song_name):
    '''
        generates search page url and then passes the correctly matched song link to song_page function
    '''
    url = "http://www.instamp3.me/download/" + "-".join(song_name.lower().split()) + ".html"
    request_obj = requests.get(url)
    plain_code = request_obj.text
    soup_obj = BeautifulSoup(plain_code, "lxml")
    for link in soup_obj.findAll('div', {'class': 'item'}):
        try:
            if 'lyric' in str(link.findNext('img')['alt']).lower() and r'Bitrate: 320 Kbps' in str(link.findNext('em')):
                print("Found Your Song. Name on net : ")
                print(str(link.findNext('img')['alt']).lower().title())
                song_page(link.findNext('a', {'class': 'downnow'})['href'], song_name)
                return
        except Exception as e:
            pass
        if r'Bitrate: 320 Kbps' in str(link.findNext('em')):
            print("Found Your Song")
            song_page(link.findNext('a', {'class': 'downnow'})['href'], song_name)
            return


def main():
    fr = open("songs_to_download.txt", "r")
    for lines in fr.readlines():
        if lines != '':
            print("Song Name : " + lines[:-1].lower().title())
            search_song(lines[:-1].lower().title())


if __name__ == '__main__':
    main()
