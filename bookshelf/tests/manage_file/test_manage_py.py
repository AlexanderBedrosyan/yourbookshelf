import subprocess
import os
from django.test import TestCase


class ManagePyBasicTests(TestCase):
    def test_manage_py_runs(self):
        result = subprocess.run(
            ['python', 'manage.py', '--help'],
            capture_output=True, text=True, cwd=os.getcwd()
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn('Type \'manage.py help <subcommand>\'', result.stdout)

