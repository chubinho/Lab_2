import os
import shutil
import tempfile

import pytest

from src.commands import get_cat, get_cd, get_cp, get_ls, get_mv, get_rm
from src.commands.archive import ArchiveCommands

archive = ArchiveCommands()


def test_cat():
    """Тест: cat выводит содержимое файла"""
    vr_dir = tempfile.mkdtemp()
    path = os.path.join(vr_dir, "test.txt")
    with open(path, "w") as f:
        f.write("123")
    get_cat([path])
    shutil.rmtree(vr_dir)


def test_cat_error():
    """Тест: cat на несуществующий файл"""
    vr_dir = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        get_cat(["/nonexistent"])

    shutil.rmtree(vr_dir)


def test_ls():
    """Тест: ls показывает файлы в директории"""

    vr_dir = tempfile.mkdtemp()
    path1 = os.path.join(vr_dir, "text1.txt")
    path2 = os.path.join(vr_dir, "text2.txt")
    with open(path1, "w") as f:
        f.write("1")
    with open(path2, "w") as f:
        f.write("1")

    get_ls([vr_dir])

    shutil.rmtree(vr_dir)


def test_ls_error():
    """Тест: ls на несуществующий путь"""

    vr_dir = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        get_ls(["/PR/pr"])

    shutil.rmtree(vr_dir)


def test_cd():
    """Тест: cd переходит в директорию"""

    old_dir = os.getcwd()
    vr_dir = tempfile.mkdtemp()

    get_cd([vr_dir])

    assert os.getcwd() == vr_dir

    os.chdir(old_dir)
    shutil.rmtree(vr_dir)


def test_cd_error():
    """Тест: cd на несуществующую директорию"""

    old_dir = os.getcwd()

    with pytest.raises(FileNotFoundError):
        get_cd(["/nonexistent"])

    os.chdir(old_dir)


def test_cp():
    """Тест: cp копирует файл"""

    vr_dir = tempfile.mkdtemp()
    src = os.path.join(vr_dir, "src.txt")
    dst = os.path.join(vr_dir, "dst.txt")
    with open(src, "w") as f:
        f.write("test")

    get_cp([src, dst])

    assert os.path.exists(dst)

    with open(dst, "r") as f:
        assert f.read() == "test"

    shutil.rmtree(vr_dir)


def test_cp_error():
    """cp на несуществующий файл"""

    vr_dir = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        get_cp(["/nonexistent", "/tmp"])

    shutil.rmtree(vr_dir)


def test_mv():
    """Тест: mv перемещает файл"""

    vr_dir = tempfile.mkdtemp()
    src = os.path.join(vr_dir, "src.txt")
    dst = os.path.join(vr_dir, "dst.txt")
    with open(src, "w") as f:
        f.write("test")

    get_mv([src, dst])

    assert not os.path.exists(src)
    assert os.path.exists(dst)

    with open(dst, "r") as f:
        assert f.read() == "test"

    shutil.rmtree(vr_dir)


def test_mv_error():
    """Тест: mv на несуществующий файл"""
    vr_dir = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        get_mv(["/nonexistent", "/tmp"])

    shutil.rmtree(vr_dir)


def test_rm():
    """Тест: rm удаляет файл"""

    vr_dir = tempfile.mkdtemp()
    file_path = os.path.join(vr_dir, "to_delete.txt")
    with open(file_path, "w") as f:
        f.write("test")

    get_rm([file_path])

    assert not os.path.exists(file_path)

    shutil.rmtree(vr_dir)


def test_rm_error():
    """Тест: rm на несуществующий файл"""

    vr_dir = tempfile.mkdtemp()

    with pytest.raises(FileNotFoundError):
        get_rm(["/nonexistent"])

    shutil.rmtree(vr_dir)
