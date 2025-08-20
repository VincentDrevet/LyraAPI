from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from enum import Enum
from datetime import datetime

class BrokerPermission(Enum):
    # MOSQ_ACL_NONE 0x00
    # MOSQ_ACL_READ 0x01
    # MOSQ_ACL_WRITE 0x02
    # MOSQ_ACL_SUBSCRIBE 0x04

    NONE = 0
    READ = 1
    WRITE = 2
    SUBSCRIBE =4


class Acl(Base):
    __tablename__ = "acls"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    topic = Column(String, nullable=False)
    permission = Column(SqlEnum(BrokerPermission))
    device_id = Column(Integer, ForeignKey('devices.id'))
    device = relationship("Device", back_populates="acls")
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)