import requests
from requests.exceptions import RequestException 
import sys,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='GB18030')

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
def parse_one_page(html):
    pattern = re.compole('')

def main():
    url = 'https://movie.douban.com/top250'
    html = get_one_page(url)
    print(html)

if __name__ == '__main__':
    main()