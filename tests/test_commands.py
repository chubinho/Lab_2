import os
import shutil
import tempfile

from src.commands import get_cat, get_cd, get_cp, get_ls, get_mv, get_rm


def test_ls_basic(capsys):
    """Тестируем ls,
    проверяем вывод файлов в директории"""
    vr_dir = tempfile.mkdtemp()
    try:
        path1 = os.path.join(vr_dir, "text1.txt")
        path2 = os.path.join(vr_dir, "text2.txt")
        with open(path1, "w") as f:
            f.write("1")
        with open(path2, "w") as f:
            f.write("1")
        get_ls([vr_dir])
        output = capsys.readouterr().out
        assert "text1.txt" in output
        assert "text2.txt" in output
        assert "text1.txt text2.txt" in output
    finally:
        shutil.rmtree(vr_dir)


def test_ls_error(capsys, caplog):
    """Проверка ls на
    несуществующий путь"""
    vr_dir = tempfile.mkdtemp()
    try:
        with caplog.at_level("ERROR"):
            get_ls(["/PR/pr"])
        output = capsys.readouterr()
        assert "ERROR: No such file or directory" in output.out
        assert "ERROR: No such file or directory" in caplog.text
    finally:
        shutil.rmtree(vr_dir)


def test_cd():
    """Проверяем работу cd"""
    old_dir = os.getcwd()
    vr_dir = tempfile.mkdtemp()
    try:
        get_cd([vr_dir])
        assert os.getcwd() == vr_dir
    finally:
        os.chdir(old_dir)
        shutil.rmtree(vr_dir)


def test_cd_error(caplog):
    """Проверяем cd на
    несуществующую директорию"""
    old_dir = os.getcwd()
    with caplog.at_level("ERROR"):
        get_cd(["/dffsfs"])
    assert "ERROR: No such file or directory" in caplog.text
    assert os.getcwd() == old_dir


def test_cat(capsys):
    """Проверяем вывод файла"""
    vr_dir = tempfile.mkdtemp()
    try:
        path = os.path.join(vr_dir, "test.txt")
        with open(path, "w") as f:
            f.write("123")
        get_cat([path])
        assert "123" in capsys.readouterr().out
    finally:
        shutil.rmtree(vr_dir)


def test_cat_files(capsys):
    """Проверяем вывод на несколько файлов"""
    vr_dir = tempfile.mkdtemp()
    try:
        path1 = os.path.join(vr_dir, "test1.txt")
        path2 = os.path.join(vr_dir, "test2.txt")
        with open(path1, "w") as f1:
            f1.write("123")
        with open(path2, "w") as f2:
            f2.write("12345")
        get_cat([path1, path2])
        output = capsys.readouterr().out
        assert "123" in output
        assert "12345" in output
    finally:
        shutil.rmtree(vr_dir)


def test_cp():
    """ПРоверяем копирование файла"""
    vr_dir = tempfile.mkdtemp()
    try:
        src = os.path.join(vr_dir, "src.txt")
        dst = os.path.join(vr_dir, "dst.txt")
        with open(src, "w") as f:
            f.write("test")
        get_cp([src, dst])
        assert os.path.exists(dst)
        with open(dst, "r") as f:
            assert f.read() == "test"
    finally:
        shutil.rmtree(vr_dir)


def test_cp_error(caplog):
    """Копирование несуществующего файла"""
    with caplog.at_level("ERROR"):
        get_cp(["/daaf", "/tmp"])
    assert "No such file or directory" in caplog.text


def test_mv():
    """Перемещение файла"""
    vr_dir = tempfile.mkdtemp()
    try:
        src = os.path.join(vr_dir, "src.txt")
        dst = os.path.join(vr_dir, "dst.txt")
        with open(src, "w") as f:
            f.write("test")

        get_mv([src, dst])

        assert not os.path.exists(src)
        assert os.path.exists(dst)
        with open(dst, "r") as f:
            assert f.read() == "test"
    finally:
        shutil.rmtree(vr_dir)


def test_mv_error(caplog):
    """Перемещение несуществующего файла"""
    with caplog.at_level("ERROR"):
        get_mv(["/nfefefo", "/tmp"])
    assert "No such file or directory" in caplog.text


def test_rm_basic():
    """Удаление файла"""
    vr_dir = tempfile.mkdtemp()
    try:
        file_path = os.path.join(vr_dir, "to_delete.txt")
        with open(file_path, "w") as f:
            f.write("test")
        get_rm([file_path])
        assert not os.path.exists(file_path)
    finally:
        shutil.rmtree(vr_dir)


def test_rm_error(caplog):
    """Удаление несуществующего файла"""
    with caplog.at_level("ERROR"):
        get_rm(["/nonexistent"])
    assert "No such file or directory" in caplog.text
