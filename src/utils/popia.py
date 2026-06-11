import hmac
import hashlib
from cryptography.fernet import Fernet

class POPIAProtector:
    def __init__(self, fernet_key: str, hmac_secret: str):
        if not fernet_key or "paste_generated" in fernet_key:
            raise ValueError("POPIA_SECRET_KEY is missing. Run: python generate_dev_fernet_key.py")
        self.fernet = Fernet(fernet_key.encode())
        self.hmac_secret = hmac_secret.encode()

    def encrypt_text(self, value):
        if value is None or str(value).strip() == "":
            return None
        return self.fernet.encrypt(str(value).strip().encode("utf-8"))

    def hash_value(self, value):
        if value is None or str(value).strip() == "":
            return None
        cleaned = str(value).strip().lower()
        return hmac.new(self.hmac_secret, cleaned.encode("utf-8"), hashlib.sha256).hexdigest()

def valid_sa_id_luhn(id_number: str) -> bool:
    digits = str(id_number).strip()
    if not digits.isdigit() or len(digits) != 13:
        return False
    total = 0
    for i, digit in enumerate(digits[::-1]):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0
