import pytest

from daskis.skeleton import fib, main

__author__ = "vsam"
__copyright__ = "vsam"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out


def test_pycommand():
    """
    Test the environment of a python execution process
    """
    import subprocess as sp
    import os

    assert os.getcwd() == '/storage/tuclocal/vsam/git/daskis'
    sp.call(['python', "tests/hello_slurm.py"])
