import mock
import requests
from werckercli.metrics import track_application_startup,default_command_name

from werckercli.tests import TestCase

track_command_usage_path = "werckercli.metrics.track_command_usage"

class MetricsTests(TestCase):

    def test_track_application_startup_fails_silently_on_ConnectionError(self):
        err = requests.ConnectionError()
        the_method = mock.Mock(side_effect=err)

        with mock.patch(track_command_usage_path, the_method) as puts:
            try:
                track_application_startup()
            except requests.ConnectionError:
                self.fail("track_application_startup didn't fail silently")


    def test_track_application_startup_calls_track_command_usage(self):
        the_method = mock.Mock()

        with mock.patch(track_command_usage_path, the_method) as puts:
            the_method.assert_called_once()


    @mock.patch("sys.argv", ['main.py'])
    def test_track_application_startup_uses_default_command_on_empty_args(self):
        the_method = mock.Mock()
        with mock.patch(track_command_usage_path, the_method) as puts:
            track_application_startup()

            the_method.assert_called_with(default_command_name, None)

