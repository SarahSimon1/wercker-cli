import os
import random
import mock

from werckercli import config

from werckercli.tests import BasicClientCase


class GetValueTests(BasicClientCase):
    template_name = "home-with-netrc"

    wercker_url = "http://localhost:" + str(random.randint(1, 65536))

    def test_get_value_wercker_url(self):

        result = config.get_value(config.VALUE_WERCKER_URL)

        self.assertEqual(result, self.wercker_url)

        os.environ.pop('wercker_url')

        result = config.get_value(config.VALUE_WERCKER_URL)
        self.assertEqual(result, config.DEFAULT_WERCKER_URL)

    def test_get_value_user_token(self):
        with mock.patch("clint.textui.puts", mock.Mock()):
            reload(config)

            result = config.get_value(config.VALUE_USER_TOKEN)

        self.assertEqual(result, "'1234567890123456789912345678901234567890'")

    def test_get_value_heroku_token(self):

        with mock.patch("clint.textui.puts", mock.Mock()) as puts:
            reload(config)
            result = config.get_value(config.VALUE_HEROKU_TOKEN)

            self.assertEqual(puts.call_count, 1)
            calls = puts.call_args_list
            self.assertTrue('0600' in calls[0][0][0])
        self.assertEqual(result, '1234567890123456789912345678901234567890')

        os.environ.pop('HOME')

        self.assertRaises(IOError, config.get_value, config.VALUE_HEROKU_TOKEN)

    def test_get_value_project_id(self):
        self.assertRaises(
            NotImplementedError,
            config.get_value,
            config.VALUE_PROJECT_ID
        )


class SetValueTests(BasicClientCase):
    template_name = 'home-with-netrc'

    def test_set_value_user_token(self):
        with mock.patch("clint.textui.puts", mock.Mock()):
            reload(config)

            config.set_value(config.VALUE_USER_TOKEN, "test@password")
            self.assertEqual(
                config.get_value(config.VALUE_USER_TOKEN),
                'test@password'
            )

    def test_set_value_project_id(self):
        self.assertRaises(
            NotImplementedError,
            config.set_value,
            config.VALUE_PROJECT_ID,
            "project_id"
        )
