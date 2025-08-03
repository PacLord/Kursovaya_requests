import urllib.parse
from yandex_disk import YandexDisk


def clean_text(input_text):
    cleaned_text = ''.join(c for c in input_text.strip() if c.isalnum())
    return cleaned_text


def main():
    disk = YandexDisk()
    original_text = input("Введите текст для изображения с котом: ")
    cleaned_text = clean_text(original_text)
    filename = f"{cleaned_text}.jpg"
    encoded_text = urllib.parse.quote(original_text)
    image_url = f"https://cataas.com/cat/says/{encoded_text}"
    folder = "PD-132"
    disk.create_directory(folder)
    disk_path = f"{folder}/{filename}"
    
    if disk.upload_file_by_url(image_url, disk_path):
        print(f"Изображение успешно загружено: {disk_path}")
        metadata_path = f"{folder}/{cleaned_text}_metadata.json"
        if disk.save_metadata_to_disk(disk_path, metadata_path):
            print(f"Метаинформация сохранена: {metadata_path}")
        else:
            print("Не удалось сохранить метаинформацию")
    else:
        print("Не удалось загрузить изображение")


if __name__ == "__main__":
    main()