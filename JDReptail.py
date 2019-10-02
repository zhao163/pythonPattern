from urllib import parse, request
from http import cookiejar
from lxml.html import etree
import time, csv, re


class Request_first():
    def __init__(self, url, keyword, page):
        self.url = url + '?keyword=' + parse.quote(keyword) + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=' + parse.quote(
            str(int(page) * 2 - 1)) + '&s=1&click=0'

        self.headers = {
            'method': 'GET',
            'authority': 'search.jd.com',
            'scheme': 'https',
            'path': '/Search?keyword=' + parse.quote(
                keyword) + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=' + parse.quote(
                str(int(page) * 2 - 1)) + '&s=' + str(48 * int(page) - 20) + '&click=0',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    def Cookie_add(self):
        self.cookie = cookiejar.CookieJar()
        self.handlex = request.HTTPCookieProcessor(self.cookie)
        self.opener = request.build_opener(self.handlex)

    def Request_get_read(self):
        self.req = request.Request(url=self.url, headers=self.headers)
        self.response = self.opener.open(self.req)
        self.html = self.response.read().decode('utf8')
        # print(self.html)

    def Get_html(self):
        return self.html

    def Crow(self):
        html = etree.HTML(self.html)

        self.html_data = html.xpath('//*[@id="J_goodsList"]/ul/li')
        self.Csv_save(self.html_data)
        return self.html_data

    @staticmethod
    def Csv_save(html_data):
        with open('JD_goods.csv', 'a', newline='', encoding='utf-8')as f:
            write = csv.writer(f)
            for data in html_data:
                if not data.xpath('div/div[@class="p-name p-name-type-2"]/a/em'):
                    p_name = data.xpath(
                        'div/div/div[2]/div[1]/div[@class="p-name p-name-type-2"]/a/em')
                    p_price = data.xpath(
                        'div/div/div[2]/div[1]/div[@class="p-price"]/strong/i/text()')
                    p_href = data.xpath(
                        'div/div/div[2]/div[1]/div/a/@href')
                    p_name1 = data.xpath(
                        'div/div/div[2]/div[2]/div[@class="p-name p-name-type-2"]/a/em')
                    # p_price1 = data.xpath(
                    #     'div/div/div[2]/div[2]/div[@class="p-price"]/strong/i/text()')
                    p_price1 = data.xpath(
                        'div/div/div[2]/div[2]/div[@class="p-price"]/strong/em/text()')
                    p_href1 = data.xpath(
                        'div/div/div[2]/div[2]/div/a/@href')
                    try:
                        p_skuid = re.findall("//item.jd.com/(.+?).html", p_href[0])
                        p_skuid1 = re.findall("//item.jd.com/(.+?).html", p_href1[0])
                    except:
                        p_skuid = []
                    if len(p_price) == 0:
                        p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')
                        p_price1 = data.xpath('div/div[@class="p-price"]/strong/@data-price')

                    try:
                        print(p_skuid[0], p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid[0], p_name[0].xpath('string(.)'), p_price[0]])
                        print(p_skuid1[0], p_name1[0].xpath('string(.)'), p_price1[0])
                        write.writerow([p_skuid1[0], p_name1[0].xpath('string(.)'), p_price1[0]])
                    except:
                        print(p_skuid, p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid, p_name[0].xpath('string(.)'), p_price[0]])
                        print(p_price1)
                        print(p_skuid1, p_name1[0].xpath('string(.)'), p_price1)
                        write.writerow([p_skuid1, p_name1[0].xpath('string(.)'), p_price1])
                else:
                    p_name = data.xpath('div/div[@class="p-name p-name-type-2"]/a/em')
                    p_price = data.xpath('div/div[@class="p-price"]/strong/i/text()')
                    p_href = data.xpath('div/div/a/@href')
                    try:
                        p_skuid = re.findall("//item.jd.com/(.+?).html", p_href[0])
                    except:
                        p_skuid = []
                    if len(p_price) == 0:
                        p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')

                    try:
                        print(p_skuid[0], p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid[0], p_name[0].xpath('string(.)'), p_price[0]])
                    except:
                        print(p_skuid, p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid, p_name[0].xpath('string(.)'), p_price[0]])
        f.close()


class Request_last(Request_first):
    def __init__(self, url, keyword, page):
        a = time.time()
        b = '%.5f' % a
        self.url = url + '?keyword=' + parse.quote(keyword) + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=' + parse.quote(
            str(int(page) * 2)) + '&s=' + str(48 * int(page) - 20) + '&scrolling=y&log_id=' + str(
            b) + '&tpl=1_M&show_items=7437788,8514651,7651931,7437780,7641991,8051124,8051104,100000503295,8264403,7652159,7652139,6735790,8782991,100001063264,4609660,7652141,7283905,5159242,7437786,100000503275,4620979,100000400010,100000503277,100000349372,7652169,8264407,7633911,8302186,8302184,7652161'

        self.headers = {
            'method': 'GET',
            'authority': 'search.jd.com',
            'scheme': 'https',
            'path': '/s_new.php?keyword=' + parse.quote(
                keyword) + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=' + parse.quote(str(int(page) * 2)) + '&s=' + str(
                48 * int(page) - 20) + '&scrolling=y&log_id=' + str(
                b) + '&tpl=1_M&show_items=7437788,8514651,7651931,7437780,7641991,8051124,8051104,100000503295,8264403,7652159,7652139,6735790,8782991,100001063264,4609660,7652141,7283905,5159242,7437786,100000503275,4620979,100000400010,100000503277,100000349372,7652169,8264407,7633911,8302186,8302184,7652161',
            'scheme': 'https',
            'accept': '*/*',
            'pragma': 'no-cache',
            'referer': 'https://search.jd.com/Search?keyword=' + parse.quote(
                keyword) + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=' + str(page) + '&s=' + str(
                48 * int(page) - 20) + '&click=0',
            'cache-control': 'no-cache',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

    def Cookie_add(self):
        self.cookie = cookiejar.CookieJar()
        self.handlex = request.HTTPCookieProcessor(self.cookie)
        self.opener = request.build_opener(self.handlex)

    def Request_get_read(self):
        self.req = request.Request(url=self.url, headers=self.headers)
        self.response = self.opener.open(self.req)
        self.html = self.response.read().decode('utf8')
        print(self.html)

    def Get_html(self):
        return self.html

    def Crow(self):
        html = etree.HTML(self.html)
        self.html_data = html.xpath('/html/body/li')
        self.Csv_save(self.html_data)
        return self.html_data

    @staticmethod
    def Csv_save(html_data):
        with open('JD_goods.csv', 'a', newline='', encoding='utf-8')as f:
            write = csv.writer(f)
            for data in html_data:
                if data.xpath('div/div[@class="p-name p-name-type-2"]/a/em'):
                    p_price = data.xpath('div/div[@class="p-price"]/strong/i/text()')
                    p_href = data.xpath('div/div[3]/a/@href')
                    try:
                        p_skuid = re.findall("//item.jd.com/(.+?).html", p_href[0])
                    except:
                        p_skuid = []
                    p_name = data.xpath('div/div[@class="p-name p-name-type-2"]/a/em')
                    if len(p_price) == 0:
                        p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')
                    try:
                        print(p_skuid[0], p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid[0], p_name[0].xpath('string(.)'), p_price[0]])
                    except:
                        print(p_skuid, p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid, p_name[0].xpath('string(.)'), p_price[0]])
                else:
                    p_name = data.xpath(
                        'div/div/div[2]/div[1]/div[@class="p-name p-name-type-2"]/a/em')
                    p_price = data.xpath(
                        'div/div/div[2]/div[1]/div[@class="p-price"]/strong/i/text()')
                    p_href = data.xpath(
                        'div/div/div[2]/div[1]/div/a/@href')
                    p_name1 = data.xpath(
                        'div/div/div[2]/div[2]/div[@class="p-name p-name-type-2"]/a/em')
                    # p_price1 = data.xpath(
                    #     'div/div/div[2]/div[2]/div[@class="p-price"]/strong/i/text()')
                    p_price1 = data.xpath(
                        'div/div/div[2]/div[2]/div[@class="p-price"]/strong/em/text()')
                    p_href1 = data.xpath(
                        'div/div/div[2]/div[2]/div/a/@href')
                    try:
                        p_skuid = re.findall("//item.jd.com/(.+?).html", p_href[0])
                        p_skuid1 = re.findall("//item.jd.com/(.+?).html", p_href1[0])
                    except:
                        p_skuid = []
                    if len(p_price) == 0:
                        p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')
                        p_price1 = data.xpath('div/div[@class="p-price"]/strong/@data-price')

                    try:
                        print(p_skuid[0], p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid[0], p_name[0].xpath('string(.)'), p_price[0]])
                        print(p_skuid1[0], p_name1[0].xpath('string(.)'), p_price1[0])
                        write.writerow([p_skuid1[0], p_name1[0].xpath('string(.)'), p_price1[0]])
                    except:
                        print(p_skuid, p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid, p_name[0].xpath('string(.)'), p_price[0]])
                        print(p_price1)
                        print(p_skuid1, p_name1[0].xpath('string(.)'), p_price1)
                        write.writerow([p_skuid1, p_name1[0].xpath('string(.)'), p_price1])
        f.close()


keyword = input('输入搜索关键词：')
j = 1
for page in range(3):
    page += 1

    a = Request_first('https://search.jd.com/Search', keyword, page)
    a.Cookie_add()
    a.Request_get_read()
    html_data = a.Crow()

    b = Request_last('https://search.jd.com/s_new.php', keyword, page)
    b.Cookie_add()
    b.Request_get_read()
    html_data = b.Crow()
