from numpy import base_repr
from bs4 import BeautifulSoup
import shutil
import os
import requests
import time

noneWorking = [0, 11809]

userhome = os.path.expanduser('~')
desktop = userhome + '/Desktop/Pictures_From_PRNSTCRN/'

if not os.path.exists(desktop):
    os.makedirs(desktop)


def get_html(code):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        response = requests.get('https://prnt.sc/' + code, headers=headers, timeout=5)
        return response.text
    except:
        time.sleep(10)
        print("ReadTimeout - Sleep for 10 sec")


def get_code(code_old):
    print("Start from: " + str(code_old))
    for i in range(int(code_old, 36), 0, -1):
        code = base_repr(i, 36).lower()
        main(code)


def main(code):
    html = get_html(code)
    soup = BeautifulSoup(html, 'lxml')

    try:
        line = soup.find('img', class_='screenshot-image')['src']

        # Get name file
        txt = line.replace('https://i.imgur.com/', '')
        txt = txt.replace('https://i.imgur.com/', '')
        txt = txt.replace('https://image.prntscr.com/image/', '')

        # Check for remove image
        if '0_173a7b_211be8ff.png' in txt:
            pass
        else:
            response = requests.get(line, stream=True)

            # Save image
            with open(desktop + txt, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            size = os.path.getsize(desktop + txt)

            # Check for remove image
            if size in noneWorking:
                print("[-] Invalid: " + str(code))
                os.remove(desktop + txt)
            else:
                print("[+] Valid: " + str(code))
    except TypeError:
        print("ERROR - TypeError - " + str(code))


if __name__ == '__main__':
    print("Enter the code after '.com /' from which the search will start: ")
    code_old = input()
    get_code(code_old)
