import random
import string
import time

from .models import VerificationCode


def send_auth_code(phone_number):
    """Создает код авторизации и сохраняет его в базе данных."""

    code = "".join(random.choices(string.digits, k=4))
    # создаем для кажого запроса новую запись, например для дальнейшей аналитики
    VerificationCode.objects.create(phone_number=phone_number, code=code)

    time.sleep(2)

    return code
