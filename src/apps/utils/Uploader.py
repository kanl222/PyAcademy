import os
from pathlib import Path
from config.settings import MEDIA_ROOT

class Uploader:

    @staticmethod
    def get_or_create_path(name:str) -> Path:
        """
        Args:
            name (str): имя файла
        Returns:
            Path: объект pathlib.Path для полученного пути
        """      
        try:
            os.mkdir(str(name))
        except FileExistsError:
            raise ValueError(f"Directory {name} already exists")
        except OSError as e:
            raise ValueError(f"Failed to create directory {name}: {e}")
        return Path(name).resolve()

    @staticmethod
    def get_path(owner: str,extension:str, filename: str):
        """
        Args:
            owner (str): имя владельца файла
            filename (str): имя файла

        Returns:
            Path: объект pathlib.Path для полученного пути
        """
        os.chdir(MEDIA_ROOT)
        owner_dir = Uploader.get_or_create_path(owner)
        file_path = owner_dir / f'{filename}.{extension}'
        return file_path.resolve()

