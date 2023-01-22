from pathlib import Path
from YandexDisk import YandexDisk
from VKontakte import VK

vk_token = ' '
vk_version = '5.131'
ya_disk_token = ' '

# vk_user_id = '738716013'
# screen_name = 'dm1try12345'


if __name__ == '__main__':
    vk = VK(vk_token, vk_version)
    vk.users_info()
    urls = vk.get_photos()
    names = vk.photos_download()
    ya_disk = YandexDisk(ya_disk_token)
    folder_name = ya_disk.create_folder()

    for name in names:
        pc_path = Path('VK_Downloads', name)
        yd_path = Path(folder_name, name)
        ya_disk.upload_file(yd_path, pc_path)

    vk.data_file()
    print("Загрузка завершена!")

