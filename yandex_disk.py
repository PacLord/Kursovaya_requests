import json
import os
import time

import requests
from dotenv import load_dotenv


class YandexDisk:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("YANDEX_DISK_TOKEN")
        self.base_url = "https://cloud-api.yandex.net/v1/disk"
        self.headers = {"Authorization": f"OAuth {self.token}"}

    def create_directory(self, path):
        url = f"{self.base_url}/resources"
        params = {"path": path}
        response = requests.put(url, headers=self.headers, params=params)
        if response.status_code in (201, 204):
            print(f"Директория '{path}' создана!")
            return True
        elif response.status_code == 409:
            print(f"Директория '{path}' уже существует, продолжаю выполнение")
            return True
        else:
            print(
                f"Ошибка при создании директории: "
                f"{response.json().get('message', 'Неизвестная ошибка')}"
            )
            return False

    def upload_file_by_url(self, url, disk_path):
        upload_url = f"{self.base_url}/resources/upload"
        params = {"url": url, "path": disk_path}
        response = requests.post(upload_url, headers=self.headers, params=params)
        if response.status_code in (202, 201):
            return True
        else:
            print(
                f"Ошибка при загрузке файла: "
                f"{response.json().get('message', 'Неизвестная ошибка')}"
            )
            return False

    def get_file_metadata(self, disk_path, max_wait=30):
        url = f"{self.base_url}/resources"
        params = {"path": disk_path}
        start_time = time.time()
        while True:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return json.dumps(response.json(), ensure_ascii=False, indent=2)
            if response.status_code == 404 and (time.time() - start_time) < max_wait:
                time.sleep(1)
                continue
            print(
                f"Ошибка при получении метаинформации: "
                f"{response.json().get('message', 'Неизвестная ошибка')}"
            )
            return None

    def save_metadata_to_disk(self, file_path, metadata_path):
        metadata = self.get_file_metadata(file_path)
        if not metadata:
            print(f"Не удалось получить метаинформацию для файла '{file_path}'")
            return False

        upload_url = f"{self.base_url}/resources/upload"
        params = {"path": metadata_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=self.headers, params=params)
        if response.status_code != 200:
            print(
                f"Ошибка при получении ссылки для загрузки: "
                f"{response.json().get('message', 'Неизвестная ошибка')}"
            )
            return False

        upload_link = response.json().get("href")
        upload_response = requests.put(
            upload_link, headers=self.headers, data=metadata.encode("utf-8")
        )
        if upload_response.status_code in (201, 202):
            return True
        else:
            print(f"Ошибка при загрузке JSON: {upload_response.status_code}")
            return False