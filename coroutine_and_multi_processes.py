from multiprocessing import Pool
from bs4 import BeautifulSoup
import time
import aiohttp
import asyncio

html_contents = {}


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
                html_contents[url] = html


def parse_text(url, html):
    soup = BeautifulSoup(html, 'html.parser')
    title = str(soup.select('.shici-title')[0].get_text())
    print(url, title, flush=True)

def main():
    domain = 'http://www.shicimingju.com'
    urlTemplate = domain + '/chaxun/zuozhe/9_{0}.html'
    pageNum = 50  # 读取50页诗词进行测试
    loop = asyncio.get_event_loop()  # 获取事件循环
    # 协程抓取网页内容 缺点是需要额外存储 本来用yield迭代，但在协程里面不知道怎么写 留坑 以后优化
    tasks = []
    for num in range(pageNum):
        tasks.append(do_task(domain, urlTemplate.format(num + 1)))
    loop.run_until_complete(asyncio.wait(tasks))  # 协程
    loop.close()
    # 多进程解析
    p = Pool(4)  # 我的CPU是八核的就用8个进程
    for url, html in html_contents.items():
        p.apply_async(parse_text, args=(url, html))
    p.close()
    p.join()  # 运行完所有子进程才能顺序运行后续程序


if __name__ == '__main__':
    start = time.time()
    main()  # 调用方
    print('总耗时：%.5f秒' % float(time.time() - start))
