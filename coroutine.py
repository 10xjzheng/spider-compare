from bs4 import BeautifulSoup
import time
import aiohttp
import asyncio
import sys

async def do_task(domain, pageUrl):
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', pageUrl) as resp:
            if resp.status != 200:
                raise Exception('http error, url:{} code:{}'.format(pageUrl, resp.status))
            html = await resp.read()  # 可直接获取bytes
    soup = BeautifulSoup(html, 'html.parser')
    for h in soup.select('h3>a'):
        url = ''.join([domain, h.get('href')])
        async with aiohttp.ClientSession() as session:
            async with session.request('GET', url) as resp:
                if resp.status != 200:
                    raise Exception('http error, url:{} code:{}'.format(pageUrl, resp.status))
                html = await resp.read()  # 可直接获取bytes
        print('url:{} title:{}'.format(url, parse_text(html)))


def parse_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return str(soup.select('.shici-title')[0].get_text())


def main():
    domain = 'http://www.shicimingju.com'
    urlTemplate = domain + '/chaxun/zuozhe/9_{0}.html'
    pageNum = 50  # 读取50页诗词进行测试
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = []
    for num in range(pageNum):
        tasks.append(do_task(domain, urlTemplate.format(num + 1)))
    loop.run_until_complete(asyncio.wait(tasks))  # 协程
    loop.close()


if __name__ == '__main__':
    start = time.time()
    main()  # 调用方
    print('总耗时：%.5f秒' % float(time.time() - start))
