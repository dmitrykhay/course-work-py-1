import requests
import os
from pathlib import Path


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, vk_token, vk_version):
        self.params = {
            'access_token': vk_token, 
            'v': vk_version
        }

    def users_info(self, vk_user_id):
        users_info_url = self.url + 'users.get'
        users_info_params = {'user_ids': vk_user_id}
        response = requests.get(users_info_url, params={**self.params, **users_info_params})
        first_name = response.json()['response'][0]['first_name']
        last_name = response.json()['response'][0]['last_name']
        print(f'Пользователь: {first_name} {last_name}\n')
        return response.json()

    def get_photos(self, vk_user_id=None):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'owner_id': vk_user_id,
            'album_id': 'profile',
            'photo_sizes': 1,
            'extended': 1,
        }
        response = requests.get(get_photos_url, params={**self.params, **get_photos_params})
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
            photo = item['sizes']
            # pprint(photo)
            for i in photo:
                if 'w' or 'z' or 'y' in i.values():
                    url = i['url']
                    item_dict['url'] = url
                    item_dict['size'] = i['type']
            urls.append(item_dict)
        print('Ссылки для скачивания фотографий в максимальном разрешении сформированы.\n')
        #pprint(urls)
        return urls

    def photos_download(self):
        if not os.path.isdir('VK_Downloads'):
            os.mkdir('VK_Downloads')
        count = 0
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
