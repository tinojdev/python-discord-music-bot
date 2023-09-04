import os
import logging

logger = logging.getLogger(__name__)


class TempHandler:
    TEMP_DIR = None
    FILENAMES_TO_DELETE = []

    @classmethod
    def get_temp_dir(cls):
        if cls.TEMP_DIR is not None:
            return cls.TEMP_DIR
        cls.TEMP_DIR = os.getenv("TEMP_DIR", None)

        if cls.TEMP_DIR is None:
            cls.TEMP_DIR = "../temp"

        return cls.TEMP_DIR

    @classmethod
    def add_file_to_delete(cls, filename):
        cls.FILENAMES_TO_DELETE.append(filename)

    @classmethod
    def rename_file_in_temp(cls, filename):
        random_name = os.urandom(24).hex()
        os.rename(os.path.join(cls.get_temp_dir(), filename), os.path.join(cls.get_temp_dir(), random_name))
        return random_name

    @classmethod
    def clear_temp_dir(cls):
        temp_dir = cls.get_temp_dir()
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))

    @classmethod
    def delete_all_to_delete_files(cls):
        if len(cls.FILENAMES_TO_DELETE) == 0:
            return
        temp_dir = cls.get_temp_dir()
        for file in cls.FILENAMES_TO_DELETE:
            try:
                os.remove(os.path.join(temp_dir, file))
                cls.FILENAMES_TO_DELETE.remove(file)
            except PermissionError:
                continue
            except Exception as e:
                logger.error("Error while deleting file: " + file)
                logger.error(e)
                cls.FILENAMES_TO_DELETE.remove(file)

    @classmethod
    def remove_from_temp_dir(cls, filename):
        temp_dir = cls.get_temp_dir()
        os.remove(os.path.join(temp_dir, filename))
