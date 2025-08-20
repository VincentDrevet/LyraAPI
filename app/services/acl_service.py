from typing import Optional, List
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy import update
from app.schemas.acl import NewAclModel, ReturnNewAclModel, GetAclModel, AclCheck
from app.models.acl import Acl, BrokerPermission
from app.models.device import Device
from app.exceptions.database import EntityNotFound
from datetime import datetime

def create_acl(db: Session, device_id: int, create_acl: NewAclModel) -> ReturnNewAclModel:

    try:
        acl = Acl(topic=create_acl.topic, permission=BrokerPermission(create_acl.permission))
        #
        # try:
        #     db.add(acl)
        #     db.commit()
        #     return ReturnNewAclModel(id=acl.id, topic=acl.topic, permission=acl.permission, device_id=acl.device_id, created_at=acl.created_at, updated_at=acl.updated_at, deleted_at=acl.deleted_at)
        # except Exception as e:
        #     db.rollback()
        #     raise e

        device: Optional[Device] = db.query(Device).filter(Device.id == device_id).first()
        if device is None:
            raise EntityNotFound({"message": f"device with id {device_id} not found"})

        device.acls.append(acl)

        db.commit()
        return device
    except:
        raise


def get_acl(db: Session, device_id: int ,acl_id: int) -> GetAclModel:

    acl: Optional[Acl] = db.query(Acl).join(Device).filter(and_(Device.id == device_id, Acl.id == acl_id)).first()

    if acl is None:
        raise EntityNotFound(details={"message" : f"No acl found for device with id {device_id} and acl id {acl_id}"})

    return GetAclModel(id=acl.id, topic=acl.topic, permission=acl.permission, created_at=acl.created_at, updated_at=acl.updated_at, deleted_at=acl.deleted_at, device_id=acl.device_id)


def get_acls(db: Session, device_id: int) -> List[GetAclModel]:

    device = db.query(Device).filter(Device.id == device_id).first()

    if device is None:
        raise EntityNotFound({"message": f"Device with id {device_id} not found."})

    acls: List[Acl] = db.query(Acl).join(Device).filter(Device.id == device_id).all()

    return list(map(lambda x: GetAclModel(id=x.id, topic=x.topic, permission=x.permission, created_at=x.created_at, updated_at=x.updated_at, deleted_at=x.deleted_at, device_id=x.device_id), acls))


def remove_acl(db: Session, device_id: int, acl_id: int):

#     Check if acl exist
    acl: Optional[Acl] = db.query(Acl).join(Device).filter(and_(Device.id == device_id, Acl.id == acl_id)).first()

    if acl is None:
        raise EntityNotFound(details={"message": f"Acl not found with id {acl_id} on device with id {device_id}"})

    try:
        query = update(Acl).where(Acl.id == acl_id).where(Acl.device_id == device_id).values({"deleted_at": datetime.now()})
        db.execute(query)
        db.commit()
    except Exception as e:
        raise e


def validate_acl(db: Session, check: AclCheck) -> bool:

    acl: Optional[Acl] = db.query(Acl).join(Device).where(and_(Device.device_name == check.clientid, Device.username == check.username, Acl.topic == check.topic, Acl.permission == BrokerPermission(check.acc), Acl.deleted_at.is_(None))).first()

    if acl is None:
        return False

    return True