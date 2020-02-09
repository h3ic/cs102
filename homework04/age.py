import datetime
from statistics import median, StatisticsError
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    response = get_friends(user_id, 'bdate')['response']['items']
    today = datetime.date.today()
    ages_list = []

    for i in range(len(response)):
        try:
            bdate = response[i]['bdate']
            if len(bdate) > 6:
                day, month, year = bdate.split('.')
                day = int(day)
                month = int(month)
                year = int(year)
            else:
                continue
            dtbdate = datetime.date(year=year, month=month, day=day)
            age = today.year - dtbdate.year - \
                ((today.month, today.day) < (dtbdate.month, dtbdate.day))
            ages_list.append(age)
        except KeyError:
            pass

    try:
        return median(ages_list)

    except StatisticsError as e:
        print(e)


if __name__ == '__main__':
    print(age_predict())
