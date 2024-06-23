import os
from os.path import isdir, basename
from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


STORAGE_DIR = './storage'
FORBIDDEN_FILES = ["README.md", ".gitignore"]

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
    
    def scan(self):
        self.files = {}
        for item in os.listdir(storage_path):
            if not isdir(item) and not item in FORBIDDEN_FILES:
                name = item
                path = storage_path / item
                file = File(name=name, path=path)
                self.files[name] = file
    
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
file_service.scan()
