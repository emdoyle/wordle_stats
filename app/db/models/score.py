from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from ..base import Base


class Score(Base):
    __tablename__ = "score"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    edition = Column(Integer)
    submitted_at = Column(DateTime, server_default=func.now())
    attempts = Column(Integer)
    raw = Column(String)

    user = relationship("User", back_populates="scores")

    def __repr__(self):
        return f"Score(id={self.id!r}, user_id={self.user_id!r}, edition={self.edition!r}, attempts={self.attempts!r})"
