from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy import (
    String,
    Uuid,
    DateTime
)
from uuid import UUID, uuid4
from datetime import datetime


class BaseModel(DeclarativeBase):

    guid: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}-{self.guid}>"

    def __str__(self):
        return f"<{self.__class__.__name__}-{self.guid}>"