from bs4 import BeautifulSoup
from backoff import get
import re


def extract_news(parser):

    raw_titles = parser.find_all('a', attrs={'class': 'storylink'})
    subtext = parser.find_all('td', attrs={'class': 'subtext'})
    news, titles, urls, authors, comments, points = [], [], [], [], [], []

    for i in range(len(raw_titles)):
        titles.append(raw_titles[i].text)
        url = raw_titles[i].find_next_sibling('span')
        try:
            url = url.text
        except AttributeError:
           url = 'N/A'
        urls.append(re.sub(r'[() ]', '', url))

        rank = subtext[i].find('span', attrs={'class': 'score'})
        try:
            points.append(rank.text.replace(' points', ''))
        except AttributeError:
            points.append('N/A')

        author = subtext[i].find('a', attrs={'class': 'hnuser'})
        try:
            authors.append(author.text)
        except AttributeError:
            authors.append('N/A')

        hide = subtext[i].find('a', string='hide')
        comment = hide.find_next_sibling('a')
        try:
            comment = comment.text
            if comment == 'discuss':
                comment = '0'
            elif 's' not in comment:
                comment = '1'
            else:
                comment = comment.replace('comments', '')
        except AttributeError:
            comment = 'N/A'

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
        url = 'https://news.ycombinator.com/news?p=' + str(max - n_pages + 2)
        n_pages -= 1
        news_list.extend(news)

    return news_list


if __name__ == '__main__':
    print(get_news(5))
