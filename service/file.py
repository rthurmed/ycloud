import os
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


STORAGE_DIR = './storage'

storage_path = Path(STORAGE_DIR)
os.makedirs(storage_path, exist_ok=True)


class FileAlreadyExistsException(BaseException):
    pass


class File:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path


class FileService:
    def __init__(self) -> None:
        self.files: dict[File] = {}
    
    def store(self, file: FileStorage):
        name = secure_filename(file.filename)
        path = storage_path / name

        if os.path.exists(path):
            raise FileAlreadyExistsException()

        file.save(path)
        self.files[name] = File(name=name, path=path)
    
    def get(self, name) -> File:
        if not name in self.files:
            raise Exception()
        return self.files[name]
    
    def get_all(self):
        return self.files.values()


file_service = FileService()
