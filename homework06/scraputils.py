import requests
from bs4 import BeautifulSoup
from backoff import get


def extract_news(parser):
    """ Extract news from a given web page """
    news = {} 

    title = parser.find('tr', attrs={'class': 'athing'})
    title_a_list = title.find_all('a')

    news['title'] = title_a_list[1].text
    news['url'] = title_a_list[2].text

    subtext = parser.find('td', attrs={'class': 'subtext'})
    subtext_a_list = subtext.find_all('a')

    comments = subtext_a_list[-1].text

    if comments == 'discuss':
        comments = '0'
    else:
        print(comments)
        comments = comments.replace('comments', '')

    news['author'] = subtext.a.text
    news['comments'] = comments.replace('\xa0', '') 
    news['points'] = subtext.span.text.replace(' points', '')

    return news

def extract_next_page(parser):
    """ Extract next page URL """

     

    return next_page


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news_list.extend(news)
        n_pages-= 1

    return news_list

if __name__ == '__main__':
    resp = requests.get('https://news.ycombinator.com/')
    soup = BeautifulSoup(resp.text, 'html.parser')
    x = extract_news(soup)
    print(x)
