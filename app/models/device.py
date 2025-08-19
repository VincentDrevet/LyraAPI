from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base
from datetime import datetime


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    device_name = Column(String, nullable=False, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    