import hashlib
import hmac
import time
from typing import Any

from module.auth.infra.config import AuthConfig

from .dto import AuthProvider, VerifiedIdentity
from .exceptions import InvalidCredentials


class TelegramAuthVerifier:
    def __init__(self, settings: AuthConfig) -> None:
        self._settings = settings

    def verify(self, payload: dict[str, Any]) -> VerifiedIdentity:
        if not self._settings.telegram_bot_token:
            msg = "Telegram auth is not configured"
            raise InvalidCredentials(msg)

        received_hash = payload.get("hash")
        auth_date = payload.get("auth_date")
        telegram_id = payload.get("id")
        if not received_hash or not auth_date or not telegram_id:
            msg = "Invalid Telegram auth payload"
            raise InvalidCredentials(msg)

        try:
            auth_timestamp = int(auth_date)
        except (TypeError, ValueError) as exc:
            msg = "Invalid Telegram auth date"
            raise InvalidCredentials(msg) from exc

        if time.time() - auth_timestamp > self._settings.telegram_auth_ttl_seconds:
            msg = "Telegram auth payload expired"
            raise InvalidCredentials(msg)

        check_string = "\n".join(
            f"{key}={value}" for key, value in sorted(payload.items()) if key != "hash" and value is not None
        )
        secret_key = hashlib.sha256(self._settings.telegram_bot_token.encode()).digest()
        expected_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_hash, str(received_hash)):
            msg = "Invalid Telegram auth hash"
            raise InvalidCredentials(msg)

        return VerifiedIdentity(
            provider=AuthProvider.TELEGRAM,
            subject=str(telegram_id),
            username=payload.get("username"),
        )
