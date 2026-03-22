import unittest
from pydantic import ValidationError

from config.settings import Settings


class TelegramProxySettingsTests(unittest.TestCase):
    def test_accepts_socks5_proxy_with_credentials_and_masks_password(self):
        settings = Settings(
            BOT_TOKEN='123:abc',
            ADMIN_IDS='1',
            TELEGRAM_PROXY_URL='socks5://user:secret@127.0.0.1:1080',
        )

        self.assertEqual(settings.TELEGRAM_PROXY_URL, 'socks5://user:secret@127.0.0.1:1080')
        self.assertEqual(settings.TELEGRAM_PROXY_SAFE_URL, 'socks5://user:***@127.0.0.1:1080')

    def test_rejects_proxy_without_port(self):
        with self.assertRaises(ValidationError):
            Settings(
                BOT_TOKEN='123:abc',
                ADMIN_IDS='1',
                TELEGRAM_PROXY_URL='socks5://127.0.0.1',
            )

    def test_rejects_unsupported_proxy_scheme(self):
        with self.assertRaises(ValidationError):
            Settings(
                BOT_TOKEN='123:abc',
                ADMIN_IDS='1',
                TELEGRAM_PROXY_URL='ftp://127.0.0.1:21',
            )


if __name__ == '__main__':
    unittest.main()
