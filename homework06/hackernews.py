from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def dd_label():
    s = session()
    label = request.query.label
    id = request.query.id
    row = s.query(News).filter(News.id == id).one()
    row.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    data = get_news(20)
    added = 0
    for i in range(len(data)):
        title = data[i]['title']
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
    redirect("/news")


@route("/classify")
def classify_news():
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)

