import os
import re
import shutil
import tempfile
import zipfile

import pytest

from src.commands.archive import ArchiveCommands

archive = ArchiveCommands()


def test_grep(capsys):
    """Нахождение текста в файле"""
    vr_dir = tempfile.mkdtemp()
    file_path = os.path.join(vr_dir, "grep_test.txt")
    with open(file_path, "w") as f:
        f.write("kkk papappap\n")
        f.write("zzz\n")

    archive.grep(["kkk", file_path])
    output = capsys.readouterr().out

    assert "kkk" in output
    shutil.rmtree(vr_dir)


def test_grep_not_found(capsys):
    """grep не находит текст"""
    vr_dir = tempfile.mkdtemp()
    file_path = os.path.join(vr_dir, "test.txt")
    with open(file_path, "w") as f:
        f.write("аавпвпв\n")

    archive.grep(["nonexistent", file_path])
    output = capsys.readouterr().out

    assert output == ""
    shutil.rmtree(vr_dir)


def test_grep_file_not_found():
    """grep на несуществующий файл"""
    vr_dir = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        archive.grep(["hello", "/nonexistent"])

    shutil.rmtree(vr_dir)


def test_grep_invalid_pattern():
    """grep с неправильным регулярным выражением"""
    vr_dir = tempfile.mkdtemp()
    file_path = os.path.join(vr_dir, "test.txt")
    with open(file_path, "w") as f:
        f.write("test")
    with pytest.raises(re.error):
        archive.grep(["[", file_path])

    shutil.rmtree(vr_dir)


def test_zip_basic():
    """zip создаёт архив"""
    vr_dir = tempfile.mkdtemp()
    folder = os.path.join(vr_dir, "folder_to_zip")
    os.mkdir(folder)
    file_path = os.path.join(folder, "test.txt")
    with open(file_path, "w") as f:
        f.write("test")
    archive_path = os.path.join(vr_dir, "archive.zip")

    archive.zip([folder, archive_path])

    assert os.path.exists(archive_path)
    shutil.rmtree(vr_dir)


def test_zip_source_not_found():
    """zip на несуществующую папку"""
    vr_dir = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        archive.zip(["/nonexistent", "/tmp/archive.zip"])

    shutil.rmtree(vr_dir)


def test_zip_not_directory():
    """zip на файл вместо папки"""
    vr_dir = tempfile.mkdtemp()
    file_path = os.path.join(vr_dir, "not_a_folder.txt")
    with open(file_path, "w") as f:
        f.write("test")

    with pytest.raises(NotADirectoryError):
        archive.zip([file_path, "/tmp/archive.zip"])

    shutil.rmtree(vr_dir)


def test_unzip_basic():
    """unzip распаковывает файл"""
    vr_dir = tempfile.mkdtemp()
    old_dir = os.getcwd()

    file_path = os.path.join(vr_dir, "test.txt")
    with open(file_path, "w") as f:
        f.write("test content")

    archive_path = os.path.join(vr_dir, "test.zip")
    with zipfile.ZipFile(archive_path, 'w') as zf:
        zf.write(file_path, "test.txt")

    extract_dir = os.path.join(vr_dir, "extracted")
    os.mkdir(extract_dir)

    try:
        os.chdir(extract_dir)
        archive.unzip([archive_path])
    finally:
        os.chdir(old_dir)

    extracted_file = os.path.join(extract_dir, "test.txt")
    assert os.path.exists(extracted_file)

    with open(extracted_file, "r") as f:
        assert f.read() == "test content"

    shutil.rmtree(vr_dir)


def test_unzip_archive_not_found():
    """unzip на несуществующий архив"""
    vr_dir = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        archive.unzip(["/nonexistent.zip"])

    shutil.rmtree(vr_dir)


def test_unzip_invalid_archive():
    """unzip на не ZIP-архив"""
    vr_dir = tempfile.mkdtemp()
    not_zip_file = os.path.join(vr_dir, "not_archive.txt")
    with open(not_zip_file, "w") as f:
        f.write("not a zip file")

    with pytest.raises(zipfile.BadZipFile):
        archive.unzip([not_zip_file])

    shutil.rmtree(vr_dir)
