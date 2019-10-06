# coding=utf8
import requests
from bs4 import BeautifulSoup
import time
import threading


def do_task(domain, pageUrl):
    response = requests.get(pageUrl)
    if response.status_code != 200:
        raise Exception('http error, url:{} code:{}'.format(pageUrl, response.status_code))
    soup = BeautifulSoup(response.content, 'html.parser')
    for h in soup.select('h3>a'):
        url = ''.join([domain, h.get('href')])
        html = requests.get(url)
        print('url:{} title:{}'.format(url, parse_text(html)))


def parse_text(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    return str(soup.select('.shici-title')[0].get_text())


def main():
    domain = 'http://www.shicimingju.com'
    urlTemplate = domain + '/chaxun/zuozhe/9_{0}.html'
    pageNum = 50  # 读取50页诗词进行测试
    threads = []
    for num in range(pageNum):
        num += 1
        # 开50个线程
        t = threading.Thread(target=do_task, name='LoopThread' + str(num), args=(domain, urlTemplate.format(num)))
        threads.append(t)
    for t in threads:
        t.start()  # 启动线程
    for t in threads:
        t.join()   # 同步线程


if __name__ == '__main__':
    start = time.time()
    main()  # 调用方
    print('总耗时：%.5f秒' % float(time.time()-start))