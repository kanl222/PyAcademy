import os
from pathlib import Path
from config.settings import MEDIA_ROOT


class Uploader:
    @staticmethod
    def get_or_create_path(name: str) -> Path:
        """
        Создает директорию с заданным именем, если она не существует.

        Args:
            name (str): Имя директории.

        Returns:
            Path: Объект pathlib.Path для полученного пути.
        """
        directory = Path(name).resolve()
        if not directory.exists():
            try:
                directory.mkdir(parents=True)
            except FileExistsError:
                raise ValueError(f"Directory {name} already exists")
            except OSError as e:
                raise ValueError(f"Failed to create directory {name}: {e}")
        return directory

    @staticmethod
    def get_path(owner: str,  filename: str) -> Path:
        """
        Возвращает полный путь к файлу, основываясь на имени владельца, расширении и имени файла.

        Args:
            owner (str): Имя владельца файла.
            filename (str): Имя файла.

        Returns:
            Path: Объект pathlib.Path для полученного пути.
        """
        os.chdir(MEDIA_ROOT)
        owner_dir = Uploader.get_or_create_path(owner)
        file_path = owner_dir / filename
        return file_path.resolve()
