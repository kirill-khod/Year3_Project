import requests
import json
import pandas as pd
import csv
import re
import spacy
import wget


def get_catalogs_wb():
    url = 'https://www.wildberries.ru/webapi/menu/main-menu-ru-ru.json'
    headers = {'Accept': "*/*", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    data = response.json()
    data_list = []
    for d in data:
        if d['name'] in ['Обувь','Электроника','Бытовая техника','Игрушки','Красота']:
            try:
                for child in d['childs']:
                    try:
                        if 'косметика' in child['name'].lower() or 'косметика' in child['seo'].lower() or child['parent']==481 or child['parent']==16107:
                            try:
                                category_name = child['name']
                                category_url = child['url']
                                shard = child['shard']
                                query = child['query']
                                data_list.append({
                                    'category_name': category_name,
                                    'category_url': category_url,
                                    'shard': shard,
                                    'query': query})
                            except:
                                continue
                    except:
                        if 'косметика' in child['name'].lower() or child['parent']==481 or child['parent']==16107:
                            try:
                                category_name = child['name']
                                category_url = child['url']
                                shard = child['shard']
                                query = child['query']
                                data_list.append({
                                    'category_name': category_name,
                                    'category_url': category_url,
                                    'shard': shard,
                                    'query': query})
                            except:
                                continue
                    if child['name'] in ['Мужская','Женская','Ноутбуки и компьютеры','Смартфоны и телефоны']:
                        try:
                            for sub_child in child['childs']:
                                if sub_child['name'] in ['Кеды и кроссовки','Ноутбуки','Смартфоны']:
                                    category_name = sub_child['name']
                                    category_url = sub_child['url']
                                    shard = sub_child['shard']
                                    query = sub_child['query']
                                    data_list.append({
                                        'category_name': category_name,
                                        'category_url': category_url,
                                        'shard': shard,
                                        'query': query})
                        except:
                            continue
            except:
                continue
    return data_list


def search_category_in_catalog(url, catalog_list):
    try:
        for catalog in catalog_list:
            if catalog['category_url'] == url.split('https://www.wildberries.ru')[-1]:
                print(f'найдено совпадение: {catalog["category_name"]}')
                name_category = catalog['category_name']
                shard = catalog['shard']
                query = catalog['query']
                return name_category, shard, query
            else:
                # print('нет совпадения')
                pass
    except:
        pass


def get_data_from_json(json_file):
    data_list = []
    for data in json_file['data']['products']:
        try:
            price = int(data["salePriceU"] / 100)
        except:
            price = 0
        data_list.append({
            'Наименование': data['name'] +" "+ data['brand'],
            #'id': data['id'],
            'Описание': "",
            'Цена': int(data["salePriceU"] / 100),
            'Ссылка': f'https://www.wildberries.ru/catalog/{data["id"]}/detail.aspx?targetUrl=BP'
        })
    return data_list


def get_content(shard, query):
    headers = {'Accept': "*/*", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    data_list = []
    for page in range(1, 5):
        url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub&dest=-1075831,-77677,-398551,12358499' \
              f'&locale=ru&page={page}' \
              f'&reg=0&regions=64,83,4,38,80,33,70,82,86,30,69,1,48,22,66,31,40&sort=popular&spp=0&{query}'
        r = requests.get(url, headers=headers)
        data = r.json()
        print(f'Добавлено позиций: {len(get_data_from_json(data))}')
        if len(get_data_from_json(data)) > 0:
            data_list.extend(get_data_from_json(data))
        else:
            print(f'Сбор данных завершен.')
            break
    return data_list

def parser():
    catalog_list = get_catalogs_wb()
    data_list=[]
    try:
        for i in range(0, len(catalog_list)):
            if(i!=11):
                print(i)
                data_list.append(get_content(shard=catalog_list[i]['shard'], query=catalog_list[i]['query']))
    except TypeError:
        print('Ошибка!')
    except PermissionError:
        print('Ошибка!')

    return data_list


if __name__ == '__main__':
    res = parser()
    keys = res[0][0].keys()
    with open('final_data.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for i in range(0,len(res)):
            dict_writer.writerows(res[i])