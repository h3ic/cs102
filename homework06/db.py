from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraputils import get_news

Base = declarative_base()
engine = create_engine('sqlite:///news.db')
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    s = session()
    data = get_news(20)
    for i in range(len(data)): 
        news = News(title=data[i]['title'], 
                  author=data[i]['author'], 
                  url=data[i]['url'], 
                  comments=data[i]['comments'], 
                  points=data[i]['points']
                  ) 
        s.add(news)
        s.commit()
    print(len(data))
