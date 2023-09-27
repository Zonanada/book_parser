from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

USERNAME_YANDEX_MAIL = getenv("USERNAME_YANDEX_MAIL")
PASSWORD_YANDEX_MAIL = getenv("PASSWORD_YANDEX_MAIL")
RECIPIENT = getenv("RECIPIENT")