import requests
from pprint import pprint


class YandexDisk:
    host = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_files_list(self):
        url = f'{self.host}/v1/disk/resources/files/'
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("get_files_list request succeed!\n")
        pprint(response.json())

    def create_folder(self, folder_name='Photos_from_VK'):
        url = f'{self.host}/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': folder_name}
        response = requests.put(url, params=params, headers=headers)
        if response.status_code == 201:
            print(f'Папка "{folder_name}" на Яндекс.Диск успешно создана.\n')
        return folder_name

    def _get_upload_link(self, path):
        url = f'{self.host}/v1/disk/resources/upload/'
        headers = self.get_headers()
        params = {'path': path, 'overwrite': True}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            print("get_upload_link request succeed!\n")
        return response.json().get('href')

    def upload_file(self, path, file_name):
        upload_link = self._get_upload_link(path)
        headers = self.get_headers()
        response = requests.put(upload_link, data=open(file_name, 'rb'), headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print(f'Фотография {file_name} успешно загружена на Яндекс.Диск в папку "Photos_from_VK".\n')
