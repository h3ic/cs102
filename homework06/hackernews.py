from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier

s = session()


@route("/")
@route('/news')
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route('/add_label/')
def dd_label():
    label = request.query.label
    id = request.query.id
    row = s.query(News).filter(News.id == id).one()
    row.label = label
    s.commit()
    redirect('/news')


@route('/update')
def update_news():
    data = get_news(2)
    added = 0
    for i, entry in enumerate(data):
        title = entry['title']
        author = entry['author']
        news_in_db = s.query(News).filter(
            News.title == title, News.author == author
        ).all()
        if len(news_in_db) == 0:
            news = News(title=entry['title'],
                        author=entry['author'],
                        url=entry['url'],
                        comments=entry['comments'],
                        points=entry['points']
                        )
            s.add(news)
            s.commit()
            added += 1

    print('News added: ', added)
    redirect('/news')


@route('/classify')
def classify_news():
    model = NaiveBayesClassifier()
    classified_news = s.query(News).filter(News.label != None).all()
    X = [entry.title for entry in classified_news]
    y = [entry.label for entry in classified_news]
    model.fit(X, y)

    news_to_classify = s.query(News).filter(News.label == None).all()
    titles = [entry.title for entry in news_to_classify]
    classification = model.predict(titles)
    news_to_arrange = zip(news_to_classify, classification)

    arranged_news = []
    for i, news in enumerate(news_to_arrange):
        entry = news[0]
        if news[1] == 'good':
            num_label = 1
        elif news[1] == 'maybe':
            num_label = 2
        elif news[1] == 'never':
            num_label = 3
        arranged_news.append((entry, num_label))
    arranged_news.sort(key=lambda x: x[1])
    recommendation = [news[0] for news in arranged_news]

    return template('news_template', rows=recommendation)


if __name__ == '__main__':
    run(host='localhost', port=8080)
