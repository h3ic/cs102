from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


s = session()

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
    data = get_news(1)
    added = 0
    for i in range(len(data)):
        title = data[i]['title']  # enumerate
        author = data[i]['author']
        news_in_db = s.query(News).filter(
            News.title == title, News.author == author
        ).all()
        if len(news_in_db) == 0:
            news = News(title=data[i]['title'],
                        author=data[i]['author'],
                        url=data[i]['url'],
                        comments=data[i]['comments'],
                        points=data[i]['points']
                        )
            s.add(news)
            s.commit()
            added += 1

    print('News added: ', added)
    redirect('/news')


@route('/classify')
def classify_news():
    model = NaiveBayesClassifier()
    X_train, y_train, news_list, arranged_news = [], [], [], []

    classified_news = s.query(News).filter(News.label != None).all()
    for i, entry in enumerate(classified_news):
        #X_train.append({})
        #X_train[i]['title'] = entry.title
        X_train.append(entry.title)
        y_train.append(entry.label)
    model.fit(X_train, y_train)

    news_to_classify = s.query(News).filter(News.label == None).all()
    for i, entry in enumerate(news_to_classify):
        news_list.append(entry.title)

    classification = model.predict(news_list)
    for i, news in enumerate(classification):
        title = news[0]
        if news[1] == 'good':
            num_label = 1
        elif news[1] == 'maybe':
            num_label = 2
        elif news[1] == 'never':
            num_label = 3
        arranged_news.append((title, num_label))

    arranged_news.sort(key=lambda x: x[1])
    for news in arranged_news:
        recommendation.append(news[0])

    return recommendation 

    #return template('news_recommendations', rows=arranged_news)

if __name__ == '__main__':
    run(host='localhost', port=8080)
    print(classify_news())
