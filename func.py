import os

from config import PATH_TO_SYNC_FOLDER
from synctodisk import SyncToDisk


def get_all_file_paths(directory: str) -> list[dict]:
    """Получить все файлы в указанной директории"""
    file_paths = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        file_paths.append(
            {
                "file_path": filepath,
                "last_modified": os.path.getmtime(filepath),
                "filename": filename,
            }
        )
    return file_paths


def detect_file_change(
    file_path: str, last_modified: float
) -> tuple[bool, float]:
    """Проверяет изменен файл"""
    current_modified = os.path.getmtime(file_path)
    return last_modified != current_modified, current_modified


def synchronize_with_disk(all_files: list[dict], my_disk: SyncToDisk):
    """Синхронизируется с диском(удаляет лишнее, добавляет отсутствующее)"""
    all_filenames = [file["filename"] for file in all_files]

    try:
        all_filenames_on_disk = [file["name"] for file in my_disk.get_info()]
    except TypeError:
        all_filenames_on_disk = None

    if all_filenames_on_disk is not None:
        files_needs_upload = set(all_filenames).difference(
            set(all_filenames_on_disk)
        )
        files_needs_to_delete = set(all_filenames_on_disk).difference(
            set(all_filenames)
        )

        for file in files_needs_to_delete:
            my_disk.delete(file)

        for file in files_needs_upload:
            my_disk.load(PATH_TO_SYNC_FOLDER + file)
