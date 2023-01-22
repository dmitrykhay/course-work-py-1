import requests
import os
import json
from pathlib import Path
from pprint import pprint


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, vk_token, vk_version):
        self.params = {
            'access_token': vk_token, 
            'v': vk_version
        }

    def screen_name_resolve(self, screen_name):
        screen_name_resolve_url = self.url + 'utils.resolveScreenName'
        screen_name_resolve_params = {'screen_name': screen_name}
        response = requests.get(screen_name_resolve_url, params={**self.params, **screen_name_resolve_params})
        if response.status_code == 200:
            print("screen_name_resolve request succeed!\n")
        vk_user_id = response.json()['response']['object_id']
        return vk_user_id

    def users_info(self):
        vk_user_id_or_screen_name = input("Введите id пользователя или его короткое имя: ")
        users_info_url = self.url + 'users.get'
        users_info_params = {'user_ids': vk_user_id_or_screen_name}
        response = requests.get(users_info_url, params={**self.params, **users_info_params})
        if response.status_code == 200:
            print("users_info request succeed!\n")
        first_name = response.json()['response'][0]['first_name']
        last_name = response.json()['response'][0]['last_name']
        print(f'Пользователь: {first_name} {last_name}\n')
        return response.json()

    def get_photos(self, vk_user_id=None):
        count = int(input("Введите количество фото, которое собираетесь загрузить: "))
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': vk_user_id,
            'album_id': 'profile',
            'photo_sizes': 1,
            'extended': 1,
            'count': count
        }
        response = requests.get(get_photos_url, params={**self.params, **get_photos_params})
        if response.status_code == 200:
            print("get_photos request succeed!\n")
        items = response.json()['response']['items']
        # pprint(items)
        global urls
        urls = []
        for item in items:
            item_dict = {}
            likes = item['likes']['count']
            item_dict['likes'] = likes
            date_time = item['date']
            item_dict['date_time'] = date_time
            for size in item['sizes']:
                if size['type'] == 'w':
                    item_dict['url'] = size['url']
                    item_dict['size'] = size['type']
                if size['type'] == 'z':
                    item_dict['url'] = size['url']
                    item_dict['size'] = size['type']
                if size['type'] == 'y':
                    item_dict['url'] = size['url']
                    item_dict['size'] = size['type']
            urls.append(item_dict)
        print('Ссылки для скачивания фотографий в максимальном разрешении сформированы.\n')
        # pprint(urls)
        return urls

    def photos_download(self):
        if not os.path.isdir('VK_Downloads'):
            os.mkdir('VK_Downloads')
        count = 0
        global names
        names = []
        for url in urls:
            name = f"{str(url['likes'])}.jpg"
            if name in names:
                name = f"{str(url['likes'])}_{str(url['date_time'])}.jpg" 
            if name in names:
                name = f"{str(url['likes'])}_{str(url['date_time'])}({str(count)}).jpg"
                count += 1
            names.append(name)
            link = url['url']
            path = Path('VK_Downloads', name) 
            with open(f'{path}', 'wb') as file:
                response = requests.get(link)
                content = response.content
                file.write(content)
            print(f'Фотография {name} успешно загружена на компьютер пользователя в папку "VK_Downloads".\n')
        return names

    def data_file(self):
        index = 0
        data = []
        for item in urls:
            item_dict = {}
            item_dict['file_name'] = names[index]
            item_dict['size'] = item['size']
            index += 1
            data.append(item_dict)
        with open('data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Файл data.json сформирован и загружен на компьютер пользователя.\n")
