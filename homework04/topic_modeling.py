import requests
import configparser
from typing import List

from stop_words import get_stop_words
import pymorphy2
import gensim
import gensim.corpora
import pyLDAvis
import pyLDAvis.gensim
import warnings
import webbrowser

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

config = configparser.ConfigParser()
config.read('config.ini')
vk = config['VK_CONFIG']
communities = config['COMMUNITIES']

rus_stop_words = get_stop_words('russian')
eng_stop_words = get_stop_words('english')
stop_words_list = rus_stop_words + eng_stop_words
additional = [word for word in vk['add_stop_words'].split(', ')]

morph = pymorphy2.MorphAnalyzer()


def get_wall(
    owner_id: str = '',
    domain: str = '',
    offset: int = 2500,
    count: int = 100,
    filter: str = 'owner',
    extended: int = 0,
    fields: str = '',
):

    add_str = f'''arr.push(API.wall.get({{'owner_id':{owner_id},'count':{count},'offset':{offset}+a*{count}}}));'''
    code = ('var a = 0;' +
            'var arr = [];' +
            'while (a != 25) {' +
            add_str +
            'a = a + 1;' +
            '};' +
            'return arr;'
            )

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                'code': code,
                'access_token': vk['access_token'],
                'v': vk['version']
            }
    )

    return response.json() 


def get_text(json) -> str:

    json = json['response']

    text = ''
    for i in range(len(json)):
        sub_json = json[i]['items']
        for j in range(len(sub_json)): 
            try:
                text_field = sub_json[j]['text']
                text += text_field
            except IndexError:
                continue

    return text


def get_words_list(raw_texts: str) -> List:

    res_text = ''
    for ch in raw_texts:
        if not ch.isalpha() and ch not in '-/\n ':
            ch = ch.replace(ch, '')
        res_text += ch

    word_list = res_text.lower().split()

    result = []
    trash = []
    for word in word_list:
        for stop in additional:
            if stop in word:
                trash.append(word)
                break

    for word in word_list:
        if word not in trash:
            if word == 'техно':
                result.append(word)
                continue
            normal = morph.parse(word)[0].normal_form
            result.append(normal)

    subtract = list(set(stop_words_list) | set(trash) | set(additional))
    result = [i for i in result + subtract if
              i in result and i not in subtract and len(i) > 2
              ]

    return result


def get_topics(word_lists: list, topics: int) -> None:

    id2word = gensim.corpora.Dictionary(word_lists)
    corpus = [id2word.doc2bow(word_list) for word_list in word_lists]

    model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=topics,
                                            per_word_topics=True,
                                            random_state=100,
                                            update_every=1,
                                            chunksize=2000,
                                            passes=10,
                                            alpha='auto')

    # pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(model, corpus, id2word)
    # pyLDAvis.display(vis)
    pyLDAvis.save_html(vis, 'lda.html')
    webbrowser.open_new_tab('lda.html')


if __name__ == '__main__':

    with open('leftfield.txt', 'r') as l:
        l = l.read()
    with open('techno.txt', 'r') as t:
        t = t.read()
    with open('idm.txt', 'r') as i:
        i = i.read()
    with open('ambient.txt', 'r') as a:
        a = a.read()
    with open('house.txt', 'r') as h:
        h = h.read()

    entire_corpus = [l, t, i, a, h]

    word_lists = []
    topics = int(input('Number of topics: '))
    
    for corpus in entire_corpus:
        word_lists.append(get_words_list(corpus))

    print(get_topics(
        word_lists,
        topics=topics))

    '''
    word_lists = []
    count = int(input('Number of posts for each community: '))
    topics = int(input('Number of topics: '))
    for domain in communities:
        id = communities[domain]
        text = (get_text(get_wall(owner_id=id, count=count)))
        if len(text) > 1:
            word_lists.append(get_words_list(text))

    print(get_topics(
        word_lists,
        topics=topics))
    '''
