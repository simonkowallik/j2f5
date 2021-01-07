import pytest
import runpy
import sys
from unittest import mock
from argparse import ArgumentError


class Test_j2cli_wrapping:
    @staticmethod
    def test_customize_specified():
        """--customize MUST NOT be specified, j2f5 raises an ArgumentError in this case"""
        with mock.patch.object(sys, "argv", ["--customize"]):
            with pytest.raises(ArgumentError):
                runpy.run_module("j2f5", run_name="__main__")

    @staticmethod
    def test_customize_inserted():
        """test that --customize is inserted by j2f5"""
        with mock.patch.object(sys, "argv", []):
            runpy.run_module("j2f5", run_name="__main__")

            assert "--customize" in sys.argv
