import requests
from bs4 import BeautifulSoup
from backoff import get
import re


def extract_news(parser):

    raw_urls = parser.find_all('span', attrs={'class': 'sitebit comhead'})
    max_news = len(raw_urls)
    raw_titles = parser.find_all('a', attrs={'class': 'storylink'},
                                 limit=max_news)
    raw_points = parser.find_all('span', attrs={'class': 'score'},
                                 limit=max_news)
    raw_authors = parser.find_all('a', attrs={'class': 'hnuser'},
                                  limit=max_news)
    raw_comments = parser.find_all('a', string=['comments'],
                                   limit=max_news)
    subtext = parser.find_all('td', attrs={'class': 'subtext'},
                              limit=max_news)
    news, titles, urls, authors, comments, points = [], [], [], [], [], []

    for i in range(max_news):
        titles.append(raw_titles[i].text)
        url_text = raw_urls[i].text
        urls.append(re.sub(r'[() ]', '', url_text))
        points.append(raw_points[i].text.replace(' points', ''))
        authors.append(raw_authors[i].text)

        subtext_a = subtext[i].find_all('a')
        comment = subtext_a[-1].text
        if comment == 'discuss':
            comment = '0'
        elif comment == '1 comment':
            comment = '1'
        else:
            comment = comment.replace('comments', '')
        comments.append(comment.replace('\xa0', ''))

        item = {}
        item['title'] = titles[i]
        item['url'] = urls[i]
        item['author'] = authors[i]
        item['comments'] = comments[i]
        item['points'] = points[i]
        news.append(item)

    return news


def get_news(n_pages=1, url='https://news.ycombinator.com/news'):

    news_list = []
    max = n_pages
    while n_pages:
        print('Collecting data from page: {}'.format(url))
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        news = extract_news(soup)
        # print(news)
        url = 'https://news.ycombinator.com/news?p=' + str(max - n_pages + 2)
        news_list.extend(news)
        n_pages -= 1

    return news_list


if __name__ == '__main__':
    print(get_news(5))
