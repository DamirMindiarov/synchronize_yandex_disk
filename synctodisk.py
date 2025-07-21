import json
import os.path

import requests
from loguru import logger
from requests.exceptions import ConnectionError


class SyncToDisk:
    def __init__(self, token: str, dirpath: str):
        self.token = token
        self.dirpath = dirpath
        self.headers = {"Authorization": f"OAuth {token}"}

    def load(self, path, log=True):
        """Загружает файл на диск по указанному пути"""
        filename = os.path.basename(path)
        url = f"https://cloud-api.yandex.net/v1/disk/resources/upload?path={self.dirpath + "/" + filename}"

        try:
            response = requests.get(url, headers=self.headers)
            link_to_load = json.loads(response.text)["href"]

            with open(path, "rb") as file:
                requests.put(link_to_load, data=file, headers=self.headers)

            if log:
                logger.info(f"Файл {filename} успешно загружен")
        except ConnectionError:
            if log:
                logger.error(f"Файл {filename} не загружен. Ошибка соединения.")
            else:
                raise ConnectionError
        except KeyError:
            logger.error(response.json()["message"])

    def reload(self, path):
        """Перезаписывает файл по указанному пути"""
        filename = os.path.basename(path)
        try:
            self.delete(filename, log=False)
            self.load(path, log=False)
            logger.info(f"Файл {filename} успешно перезаписан")
        except ConnectionError:
            logger.error("Файл не перезаписан. Ошибка соединения")

    def delete(self, filename, log=True):
        """Удаляет файл и очищает корзину"""
        path_to_file = os.path.join(self.dirpath, filename).replace("\\", "/")
        url = f"https://cloud-api.yandex.net/v1/disk/resources?path={path_to_file}"
        url_trash = "https://cloud-api.yandex.net/v1/disk/trash/resources"

        try:
            requests.delete(url, headers=self.headers)
            requests.delete(url_trash, headers=self.headers)
            if log:
                logger.info(f"Файл {filename} успешно удален")
        except ConnectionError:
            if log:
                logger.error(f"Файл {filename} не удален. Ошибка соединения.")
            else:
                raise ConnectionError

    def get_info(self):
        """Получает информацию о файлах по указанному пути"""
        url = f"https://cloud-api.yandex.net/v1/disk/resources?path={self.dirpath}&limit=999999999999999999"
        try:
            response = requests.get(url, headers=self.headers)
            return response.json()["_embedded"]["items"]
        except ConnectionError:
            logger.error("Ошибка соединения")
        except KeyError:
            logger.error(response.json()["message"])
