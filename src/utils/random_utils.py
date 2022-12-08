import string
from secrets import choice as secrets_choice


def generate_string(length: int = 16) -> str:
    """Сгенерировать случайную строку.

    Args:
        length: длина. По умолчанию 16

    Returns:
        str: строка

    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets_choice(alphabet) for _ in range(length))
