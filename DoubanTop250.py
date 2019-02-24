import requests
from requests.exceptions import RequestException 
import sys,io
import re
import json

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
    pattern = re.compile('<li>.*?em class.*?>(\d+)</em>.*?src="(.*?)".*?title">(.*?)</span>'
                         +'.*?average">(.*?)</span>.*?inq">(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern,html)
    # print(items)
    for item in items:
        yield{
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'score':item[3],
            'comment':item[4]
        }
def writer_to_file(content):
    with open(r'C:/Users/AOAO/Desktop/doubanTop250.csv','a',encoding='gb18030') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()
def main():
    url = 'https://movie.douban.com/top250'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        writer_to_file(item)
    # print(html)

if __name__ == '__main__':
    for i in range(10)
    main(i*25)