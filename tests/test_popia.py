from cryptography.fernet import Fernet
from src.utils.popia import POPIAProtector, valid_sa_id_luhn

def test_encrypt_text_returns_bytes_and_not_plaintext():
    key = Fernet.generate_key().decode()
    protector = POPIAProtector(key, "test-secret")
    encrypted = protector.encrypt_text("Thabo")
    assert isinstance(encrypted, bytes)
    assert encrypted != b"Thabo"

def test_hash_value_is_repeatable_case_insensitive():
    key = Fernet.generate_key().decode()
    protector = POPIAProtector(key, "test-secret")
    assert protector.hash_value("ABC") == protector.hash_value("abc")

def test_valid_sa_id_luhn_accepts_valid_sample():
    assert valid_sa_id_luhn("9001015009081") is True

def test_valid_sa_id_luhn_rejects_invalid_sample():
    assert valid_sa_id_luhn("1234567890123") is False
