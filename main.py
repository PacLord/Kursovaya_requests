from yandex_disk import YandexDisk


def clean_text(input_text: str) -> str:
    return input_text.strip().replace(" ", "_")


if __name__ == "__main__":
    disk = YandexDisk()

    text = clean_text(input("Введите текст для изображения с котом: "))
    filename = f"{text}.jpg"
    image_url = f"https://cataas.com/cat/says/{text}"

    folder = "PD-132"
    disk.create_directory(folder)

    disk_path = f"{folder}/{filename}"

    if disk.upload_file_by_url(image_url, disk_path):
        print(f"Изображение успешно загружено: {disk_path}")

        metadata_path = f"{folder}/{text}_metadata.json"
        if disk.save_metadata_to_disk(disk_path, metadata_path):
            print(f"Метаинформация сохранена: {metadata_path}")
        else:
            print("Не удалось сохранить метаинформацию")
    else:
        print("Не удалось загрузить изображение")