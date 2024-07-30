from sqlalchemy import ForeignKey

from database import Base, User
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Pin(Base):
    __tablename__ = "pin"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    desc: Mapped[str]
    file: Mapped[str]
    # tags: Mapped[list['Tag']] = relationship("Tag", back_populates="tags")
    creator: Mapped[int] = mapped_column(ForeignKey("user.id"))