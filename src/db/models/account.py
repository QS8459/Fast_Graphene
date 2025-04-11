from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    String
)
from src.db.models.base import BaseModel
from passlib.hash import pbkdf2_sha256 as sha256


class Account(BaseModel):
    __tablename__ = 'account'

    email: Mapped[str] = mapped_column(
        String(),
        nullable=False,
        unique=True
    )
    password: Mapped[str] = mapped_column(
        String(),
        nullable=False
    )

    def set_pwd(self, password: str) -> None:
        self.password = sha256.using().hash(password)

    def ver_pwd(self, password: str) -> bool:
        return sha256.verify(password, self.password)


__all__ = "Account"
