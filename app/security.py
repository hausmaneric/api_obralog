import base64
import hashlib
import hmac


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


def create_access_token(user_id: int, company_id: int, role: str) -> str:
    payload = f"{user_id}:{company_id}:{role}"
    return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8")
