import os
import shutil
import tempfile

from src.commands import get_cat, get_ls


def test_ls(capsys):
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
    vr_dir = tempfile.mkdtemp()
    try:
        with caplog.at_level("ERROR"):
            get_ls(["/PR/pr"])

        output = capsys.readouterr()
        assert "ERROR: No such file or directory" in output.out
        assert "ERROR: No such file or directory" in caplog.text
    finally:
        shutil.rmtree(vr_dir)


def test_cat_error(capsys):
    vr_dir = tempfile.mkdtemp()
    try:
        path = os.path.join(vr_dir, "test.txt")
        with open(path, "w") as f:
            f.write("123")
        get_cat([path])
        assert "123" in capsys.readouterr().out
    finally:
        shutil.rmtree(vr_dir)


def test_cat(capsys):
    vr_dir = tempfile.mkdtemp()
    try:
        path1 = os.path.join(vr_dir, "test1.txt")
        path2 = os.path.join(vr_dir, "test2.txt")
        path3 = os.path.join(vr_dir, "test3.txt")
        with open(path1, "w") as f1:
            f1.write("123")
        with open(path2, "w") as f2:
            f2.write("12345")
        with open(path3, "w") as f3:
            f3.write("1")
        get_cat([path1, path2])
        output = capsys.readouterr().out
        assert "123" in output
        assert "12345" in output
        assert "1" in output
    finally:
        shutil.rmtree(vr_dir)
