import sys
import unittest
from io import StringIO
from unittest.mock import patch

from cli_interpreter.cli_repl import REPL


class TestREPL(unittest.TestCase):

    def test_echo_and_exit(self):
        repl = REPL()

        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            sys.stdin = StringIO("echo 1\nexit\n")
            try:
                repl.run()
            except SystemExit:
                pass

        output = fake_out.getvalue()
        self.assertIn("1", output)
