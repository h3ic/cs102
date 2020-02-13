from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraputils import get_news
import sys

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

def fill_db(n_pages):
    decision = input('Proceed? This will overwrite the existing news.db! y/n? ')
    if decision == 'y':
        pass
    elif decision == 'n':
        sys.exit()
    else:
        sys.exit('Bad input')

    s = session()
    data = get_news(n_pages)
    for i in range(len(data)): 
        news = News(title=data[i]['title'], 
                  author=data[i]['author'], 
                  url=data[i]['url'], 
                  comments=data[i]['comments'], 
                  points=data[i]['points']
                  ) 
        s.add(news)
        s.commit()
    print('News added: ', len(data))

if __name__ == '__main__':
    fill_db(20)
