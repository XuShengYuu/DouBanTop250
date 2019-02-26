import requests
from requests.exceptions import RequestException 
import sys,io
import re
import json
from lxml import etree
import random

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='GB18030')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def get_proxy_page():
    ip_url ='http://www.xicidaili.com/nn/'
    try:
        ip_response = requests.get(ip_url,headers=headers)
        if ip_response.status_code ==200:
            return ip_response.text
        return None
    except RequestException:
        return None

def parse_ip_page(ip_html):
    ip_list = []
    r = etree.HTML(ip_html)
    ips = r.xpath('//*[@id="ip_list"]/tr/td[2]/text()')
    # ip_pattern = re.compile('<tr class="odd".*?<td>(.*?)</td>.*?</tr>',re.S)
    # ips = re.findall(pattern,ip_html)
    # print(ips)
    for ip in ips:
        try:
            proxy = {'http':ip}
            text_url = 'https://www.baidu.com/'
            res = requests.get(url=text_url,proxies=proxy,headers=headers,timeout=1)
            ip_list.append(ip)
        except BaseException as e:
            print(e)
    # print(ip_list)
    proxies= {'http':random.choice(ip_list)}   
    print(proxies) 
    return proxies


def get_one_page(url,proxies):
        try:
            response = requests.get(url,headers=headers,proxies=proxies)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None
    # print(proxies)
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
    ip_html = get_proxy_page()
    parse_ip_page(ip_html)
    proxies = parse_ip_page(ip_html)
    # print(proxies)
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}'.format(i*25)
        html = get_one_page(url,proxies)
        for item in parse_one_page(html):
            print(item)
            writer_to_file(item)
    # print(html)
    # print(proxies)

if __name__ == '__main__':
        main()