import unittest
from unittest.mock import MagicMock, call, patch

from bakerlib.singularity_build import SingularityBaker, SingularityBakingError, SingularityExecutor

AN_OUTPUT_DIR = "AN_OUTPUT_DIR"

AN_IMAGE = "AN_IMAGE"
ANOTHER_IMAGE = "ANOTHER_IMAGE"
AN_IMAGE_WITH_NO_SOFTWARE = "AN_IMAGE_WITH_NO_SOFTWARE"

A_URL = "A_URL"
ANOTHER_URL = "ANOTHER_URL"

A_SOFTWARE = {
    "image": AN_IMAGE,
    "url": A_URL
}
ANOTHER_SOFTWARE = {
    "image": ANOTHER_IMAGE,
    "url": ANOTHER_URL
}

A_CONFIG = ["A_CONFIG"]


class TestSingularityBaker(unittest.TestCase):

    def setUp(self):
        self.mock_config = MagicMock()
        self.mock_executor = MagicMock()
        self.mock_config.environment_for.side_effect = lambda arg: A_CONFIG if arg == A_SOFTWARE else []
        self.under_test = SingularityBaker(AN_OUTPUT_DIR, self.mock_config, [A_SOFTWARE, ANOTHER_SOFTWARE],
                                           self.mock_executor)

    def test_should_bake_images(self):
        self.under_test.bake(AN_IMAGE)
        self.assertCountEqual(self.mock_executor.execute.call_args_list, [
            call(AN_OUTPUT_DIR, A_CONFIG, A_SOFTWARE)])

    def test_should_bake_image_without_config(self):
        self.under_test.bake(ANOTHER_IMAGE)
        self.assertCountEqual(self.mock_executor.execute.call_args_list, [
            call(AN_OUTPUT_DIR, [], ANOTHER_SOFTWARE)])

    def test_should_fail_if_no_corresponding_software(self):
        with self.assertRaises(SingularityBakingError) as _:
            self.under_test.bake(AN_IMAGE_WITH_NO_SOFTWARE)


class TestSingularityExecutor(unittest.TestCase):

    def setUp(self):
        self.under_test = SingularityExecutor()
        self.process_mock = MagicMock()

    @patch('subprocess.Popen')
    def test_execute_with_config(self, mock_subproc_popen):
        mock_subproc_popen.return_value = self.process_mock
        self.under_test.execute(AN_OUTPUT_DIR, A_CONFIG, A_SOFTWARE)
        expected_command = "rm -f 'AN_OUTPUT_DIR/AN_IMAGE';A_CONFIG;singularity build 'AN_OUTPUT_DIR/AN_IMAGE' 'A_URL'"
        self.assertCountEqual(mock_subproc_popen.call_args_list, [call(expected_command, shell=True)])
        self.assertEqual(self.process_mock.wait.call_count, 1)

    @patch('subprocess.Popen')
    def test_execute_without_config(self, mock_subproc_popen):
        mock_subproc_popen.return_value = self.process_mock
        self.under_test.execute(AN_OUTPUT_DIR, [], A_SOFTWARE)
        expected_command = "rm -f 'AN_OUTPUT_DIR/AN_IMAGE';singularity build 'AN_OUTPUT_DIR/AN_IMAGE' 'A_URL'"
        self.assertCountEqual(mock_subproc_popen.call_args_list, [call(expected_command, shell=True)])
        self.assertEqual(self.process_mock.wait.call_count, 1)
