import requests
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
vk = config['VK_CONFIG']


def get(url, params={}, timeout=500, max_retries=10, backoff_factor=0.3):
    """
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    try:
        response = requests.get(url, timeout=timeout)
        return response
    except requests.exceptions.RequestException as re_err:
        for i in range(max_retries - 1):
            try:
                delay = backoff_factor * (2 ** i)
                time.sleep(delay)
                response = requests.get(url)
                return response
            except requests.exceptions.RequestException:
                continue
        raise re_err
    except requests.exceptions.ConnectionError as c_err:
        raise c_err
    except requests.exceptions.HTTPError as http_err:
        raise http_err
    except requests.exceptions.ReadTimeout as rt_err:
        raise rt_err


def get_friends(user_id, fields):
    """
    :param user_id: идентификатор пользователя
    :param fields: список полей для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    domain = vk['domain']
    access_token = vk['access_token'] 
    v = vk['version']

    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"

    response = get(query)

    return response.json()


if __name__ == '__main__':
    print(get_friends())
