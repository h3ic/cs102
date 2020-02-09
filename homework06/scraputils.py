import requests
from bs4 import BeautifulSoup
from backoff import get
import re 


def extract_news(parser):

    raw_urls = parser.find_all('span', attrs={'class': 'sitebit comhead'})
    if len(raw_urls) < 30:
        return None
    raw_titles = parser.find_all('a', attrs={'class': 'storylink'})
    raw_points = parser.find_all('span', attrs={'class': 'score'})
    raw_authors = parser.find_all('a', attrs={'class': 'hnuser'})
    raw_comments = parser.find_all('a', string=['comments'])
    subtext = parser.find_all('td', attrs={'class': 'subtext'})
    news, titles, urls, authors, comments, points = [], [], [], [], [], []

    for i in range(30):
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

def extract_next_page(parser):

     
    return next_page


def get_news(url, n_pages=1):

    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news_list.extend(news)
        n_pages -= 1

    return news_list

if __name__ == '__main__':
    resp = requests.get('https://news.ycombinator.com/')
    soup = BeautifulSoup(resp.text, 'html.parser')
    x = extract_news(soup)
    print(x)
