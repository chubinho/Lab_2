import os
import shutil
import tempfile
import zipfile

from src.archive import ArchiveCommands

archive = ArchiveCommands()


def test_grep(capsys):
    """grep находит текст в файле"""
    vr_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(vr_dir, "grep_test.txt")
        with open(file_path, "w") as f:
            f.write("kkk papappap\n")
            f.write("zzz\n")
        archive.grep(["kkk", file_path])
        output = capsys.readouterr().out
        assert "kkk" in output
    finally:
        shutil.rmtree(vr_dir)


def test_grep_not_found(capsys):
    """grep не находит несуществующий текст"""
    vr_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(vr_dir, "test.txt")
        with open(file_path, "w") as f:
            f.write("hello world\n")

        archive.grep(["nonexistent", file_path])
        output = capsys.readouterr().out

        assert output == ""
    finally:
        shutil.rmtree(vr_dir)


def test_zip():
    """Проверяем создание архива"""
    vr_dir = tempfile.mkdtemp()
    try:
        folder = os.path.join(vr_dir, "folder_to_zip")
        os.mkdir(folder)
        file_path = os.path.join(folder, "test.txt")
        with open(file_path, "w") as f:
            f.write("test")
        archive_path = os.path.join(vr_dir, "archive.zip")
        archive.zip([folder, archive_path])

        assert os.path.exists(archive_path)
    finally:
        shutil.rmtree(vr_dir)


def test_unzip():
    """Пробуем распаковать файл"""
    vr_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()
    try:
        file_path = os.path.join(vr_dir, "test.txt")
        with open(file_path, "w") as f:
            f.write("test content")

        # Создаем архив из файла
        archive_path = os.path.join(vr_dir, "test.zip")

        with zipfile.ZipFile(archive_path, 'w') as zf:
            zf.write(file_path, "test.txt")

        # Распаковываем
        extract_dir = os.path.join(vr_dir, "extracted")
        os.mkdir(extract_dir)
        os.chdir(extract_dir)

        archive.unzip([archive_path])

        # Проверяем распаковку
        extracted_file = os.path.join(extract_dir, "test.txt")
        assert os.path.exists(extracted_file), f"Файл не найден: {extracted_file}"

        with open(extracted_file, "r") as f:
            assert f.read() == "test content"

    finally:
        os.chdir(old_dir)
        shutil.rmtree(vr_dir)
