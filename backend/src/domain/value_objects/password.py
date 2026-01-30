

from dataclasses import dataclass
from passlib.context import CryptContext

# Contexto do bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_BYTES = 72  # limite do bcrypt

@dataclass(frozen=True, slots=True)
class Password:
    hashed: str

    @classmethod
    def create(cls, plain: str) -> "Password":
        # Trunca para 72 bytes UTF-8
        password_bytes = plain.encode("utf-8")[:MAX_BCRYPT_BYTES]
        hashed = pwd_context.hash(password_bytes)
        return cls(hashed=hashed)

    def verify(self, plain: str) -> bool:
        password_bytes = plain.encode("utf-8")[:MAX_BCRYPT_BYTES]
        return pwd_context.verify(password_bytes, self.hashed)
