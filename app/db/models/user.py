from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    display_name = Column(String, server_default="", nullable=False)
    real_name = Column(String, server_default="", nullable=False)

    scores = relationship("Score", back_populates="user")

    def __repr__(self):
        return (
            f"User(id={self.id!r}, username={self.username!r}, "
            f"display_name={self.display_name!r}, real_name={self.real_name!r})"
        )
