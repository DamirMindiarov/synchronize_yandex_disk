import time

from loguru import logger

from config import (
    TOKEN_DISK,
    PATH_TO_SYNC_FOLDER,
    PATH_TO_FOLDER_IN_DISK,
    PERIOD_SYNC,
    PATH_TO_LOG_FILE,
)
from func import get_all_file_paths, detect_file_change, synchronize_with_disk
from synctodisk import SyncToDisk

logger.add(f"{PATH_TO_LOG_FILE}/file.log", format="{time} {level} {message}")


def main():
    my_disk = SyncToDisk(token=TOKEN_DISK, dirpath=PATH_TO_FOLDER_IN_DISK)

    all_files = get_all_file_paths(PATH_TO_SYNC_FOLDER)
    synchronize_with_disk(all_files, my_disk)

    while True:

        for file in all_files:
            try:
                changed, last_modified = detect_file_change(
                    file_path=file["file_path"],
                    last_modified=file["last_modified"],
                )
                file["last_modified"] = last_modified
                if changed:
                    my_disk.reload(path=file["file_path"])
            except FileNotFoundError:
                continue

        all_files = get_all_file_paths(PATH_TO_SYNC_FOLDER)
        synchronize_with_disk(all_files, my_disk)

        time.sleep(PERIOD_SYNC)


if __name__ == "__main__":
    logger.info(
        f"Программа синхронизации файлов начинает работу с директорией {PATH_TO_SYNC_FOLDER}"
    )

    try:
        main()
    except KeyboardInterrupt:
        logger.info("Программа синхронизации файлов завершила работу")
