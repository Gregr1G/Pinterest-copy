from Pins.database import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

class Pin(Base):
    __tablename__ = "pins"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    desc: Mapped[str]
    file: Mapped[str]