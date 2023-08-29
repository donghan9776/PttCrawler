import requests
from bs4 import BeautifulSoup
import time
import json
import datetime

start = 1
end = 100
arts_list = []
kanban = 'Gossiping'

cookies = {'over18': '1'}


def main():

    for index in range(start, end + 1, 1):

        next_url = 'https://www.ptt.cc/bbs/' + \
            kanban + '/index' + str(index) + '.html'
        resp = get_resp(next_url)
        if resp:
            get_articles(resp)
        else:
            print("404 not found")

        time.sleep(2)
        current_datetime = datetime.datetime.now()
        current_date = datetime.datetime.now().date()  # 使用你的日期
        formatted_date = current_date.strftime("%y%m%d")
        log(f'{current_datetime},已完成第 {index} 頁下載', formatted_date)


def get_resp(url):

    resp = requests.get(url, cookies=cookies)
    if resp.status_code == 200:
        return resp
    else:
        return None


def get_articles(resp):
    global arts_list
    soup = BeautifulSoup(resp.text, 'html5lib')  # 選擇解析器，resp.text為html
    arts = soup.find_all('div', class_='r-ent')  # 與class關鍵字區分，class_為CSS

    for art in arts:
        user = art.find(class_='author')
        a_tag = art.find('a')
        if user and a_tag:
            print('作者:' + user.text)
            print(a_tag.text.strip(), end=':')
            print('https://www.ptt.cc' + a_tag['href'] + '\n')
            article_url = 'https://www.ptt.cc' + a_tag['href']
            content, build_time = get_article_content(article_url)
            print(content)
            artcle = {
                'author': user.text.strip(),
                'title': a_tag.text.strip(),
                'link': article_url,
                'build_time': build_time,
                'content': content
            }
        arts_list.append(artcle)

    with open('PttData.json', 'w', encoding='utf-8') as file:
        json.dump(arts_list, file, ensure_ascii=False, indent=4)


def get_article_content(article_url):
    a = b = ''  # 暫時存放 build_time 與 article_content 的字串
    resp = requests.get(article_url, cookies=cookies)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html5lib')
        article_content = soup.find('div', class_='bbs-screen bbs-content')

        date_elements = soup.find_all('span', class_='article-meta-value')
        if len(date_elements) >= 4:
            build_time = date_elements[3]
            b = build_time.text.strip()
        else:
            b = '查無時間'
        a = article_content.text.strip()

        if article_content:
            return a, b
        else:
            return "暫無內容"


def log(data, time):
    with open(f'{time}.log', 'a') as file:
        file.write(data + '\n')


if __name__ == "__main__":
    main()
