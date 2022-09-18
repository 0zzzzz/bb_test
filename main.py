import re
from typing import List

import pymongo
import datetime


def user_input_verification(keys: list, text: str) -> list[str] | str:
    """Верификация введенных пользователем данных"""
    user_input_keys = [word for word in re.split("[^a-zA-Z{_}]", text) if word.startswith('{') or word.endswith('}')]
    errors_list = []
    for word in user_input_keys:
        if word[0] != '{':
            errors_list.append(f'{word}: Отсутствует открывающая скобка ключа')
        if word[-1] != '}':
            errors_list.append(f'{word}: Отсутствует закрывающая скобка ключа')
        if word[1:-1] not in keys:
            errors_list.append(f'Ключ {word} отсутствует в списке')
            # Или AssertionError
            # assert word[0] == '{'
            # assert word[-1] == '}'
            # assert word[1:-1] in keys
    if errors_list:
        return errors_list
    return 'Все проверки прошили успешно'


def equal_lists(arr: list) -> list:
    """Группирует повторяющиеся данные"""
    interim_dict = {tuple(i): arr.count(i) for i in arr}.items()
    final_list = []
    # здесь почему-то append не заработал в list comprehension
    # final_list = [list(i[0]).append(i[1]) for i in interim_dict]
    for i in interim_dict:
        middle = list(i[0])
        middle.append(i[1])
        final_list.append(middle)
    return final_list


def json_diff(initial_dict: dict, end_dict: dict, diff_list: list) -> dict:
    """Ищет разницу между двумя json"""
    result_dict = dict()
    for i in diff_list:
        if initial_dict['data'][i] != end_dict['data'][i]:
            result_dict[i] = end_dict['data'][i]
    return result_dict


def mongo_data_cleaning_counter(collection: pymongo.collection, data_lifetime: int) -> str:
    """Очищает данные из MongoDB по истечению заданного времени"""
    collection.create_index('date', expireAfterSeconds=data_lifetime)
    return f'Время жизни данных установлено на {data_lifetime} сек.'


def drop_indexes() -> str:
    """Сбрасывает все инндексы """
    collections.drop_indexes()
    return f'Все индексы базы данных сброшены'


def test(number: int) -> str:
    return f'Вы ввели {number}'


if __name__ == '__main__':
    print(f'1')
    list_keys = ['name', 'day_month', 'day_of_week', 'start_time', 'end_time', 'master', 'services']
    test_text = '''{name}, ваша запись изменена:
    ⌚️ {day_month} в {start_time}
    👩 {master}
    Услуги:
    {services}
    управление записью {record_link}'''
    print(user_input_verification(list_keys, test_text))
    print(f'______________')

    print(f'2')
    a = [['665587', 2], ['669532', 1], ['669537', 2], ['669532', 1], ['665587', 1], ['11', 22], ['11', 22],
         ['11', 22]] * 6
    print(equal_lists(a))
    print(f'______________')

    print(f'3')
    diff_list = ['services', 'staff', 'datetime']
    json_old = {'company_id': 111111, 'resource': 'record', 'resource_id': 406155061, 'status': 'create',
                'data': {'id': 11111111, 'company_id': 111111, 'services': [
                    {'id': 9035445, 'title': 'Стрижка', 'cost': 1500, 'cost_per_unit': 1500, 'first_cost': 1500,
                     'amount': 1}], 'goods_transactions': [], 'staff': {'id': 1819441, 'name': 'Мастер'},
                         'client': {'id': 130345867, 'name': 'Клиент', 'phone': '79111111111',
                                    'success_visits_count': 2, 'fail_visits_count': 0}, 'clients_count': 1,
                         'datetime': '2022-01-25T11:00:00+03:00', 'create_date': '2022-01-22T00:54:00+03:00',
                         'online': False, 'attendance': 0, 'confirmed': 1, 'seance_length': 3600, 'length': 3600,
                         'master_request': 1, 'visit_id': 346427049, 'created_user_id': 10573443, 'deleted': False,
                         'paid_full': 0, 'last_change_date': '2022-01-22T00:54:00+03:00', 'record_labels': '',
                         'date': '2022-01-22 10:00:00'}}
    json_new = {'company_id': 111111, 'resource': 'record', 'resource_id': 406155061, 'status': 'create',
                'data': {'id': 11111111, 'company_id': 111111, 'services': [
                    {'id': 22222225, 'title': 'Стрижка', 'cost': 1500, 'cost_per_unit': 1500, 'first_cost': 1500,
                     'amount': 1}], 'goods_transactions': [], 'staff': {'id': 1819441, 'name': 'Мастер'},
                         'client': {'id': 130345867, 'name': 'Клиент', 'phone': '79111111111',
                                    'success_visits_count': 2, 'fail_visits_count': 0}, 'clients_count': 1,
                         'datetime': '2022-01-25T13:00:00+03:00', 'create_date': '2022-01-22T00:54:00+03:00',
                         'online': False, 'attendance': 2, 'confirmed': 1, 'seance_length': 3600, 'length': 3600,
                         'master_request': 1, 'visit_id': 346427049, 'created_user_id': 10573443, 'deleted': False,
                         'paid_full': 1, 'last_change_date': '2022-01-22T00:54:00+03:00', 'record_labels': '',
                         'date': '2022-01-22 10:00:00'}}
    print(json_diff(json_old, json_new, diff_list))
    print(f'______________')

    print(f'4')
    """"""
    # подключаемся к базе
    db_client = pymongo.MongoClient('localhost', 27017)
    current = db_client['test']
    collections = current['test']
    # добавляем проверочные данные
    utc_timestamp = datetime.datetime.utcnow()
    collections.insert_one({'id': 4, "date": utc_timestamp})
    # print(collections.find_one({'id': 4}))
    # print(drop_indexes())
    print(mongo_data_cleaning_counter(collections, 24 * 60 * 60))
    # print(drop_indexes())
