import traceback

from sqlalchemy.orm import Session
from app.models import device
from app.schemas.device import DeviceAuthValidation, DeviceCreationModel, ReturnNewDeviceModel, GetDeviceModel
from app.core.security import hash_password, generate_random_password
from app.core.config import DEVICE_PASSWORD_SIZE
from app.dependencies import logger
from typing import List, Optional
from app.core.security import pwd_context


def validate_device_auth(db: Session, device_auth: DeviceAuthValidation) -> bool:


    device_db = db.query(device.Device).where(device.Device.device_name == device_auth.client_id).first()

    # Device not found
    if device_db is None:
        return False


    if (device_db.username == device_auth.username) and pwd_context.verify(device_auth.password, device_db.password):
        return True

    return False

def create_device(db: Session, new_device: DeviceCreationModel) -> ReturnNewDeviceModel:

    password = generate_random_password(int(DEVICE_PASSWORD_SIZE))

    inserted_device = device.Device(device_name=new_device.device_name, username=new_device.username, password=hash_password(password))

    try:
        db.add(inserted_device)
        db.commit()
        # The clear password is returned only after that the device has been inserted inside the database. It's the only moment where we provide the clear password.
        return ReturnNewDeviceModel(id=inserted_device.id, device_name=inserted_device.device_name, username=inserted_device.username, clear_password=password, created_at=inserted_device.created_at, updated_at=inserted_device.updated_at, deleted_at=inserted_device.deleted_at)
    except Exception as e:
        db.rollback()
        raise e

def list_device(db: Session) -> List[GetDeviceModel]:

    devices = db.query(device.Device).all()

    return list(map(__Device_to_GetDeviceModel, devices))

def get_device_by_id(db: Session, id: int) -> Optional[GetDeviceModel]:

    searched_device = db.query(device.Device).where(device.Device.id == id).first()

    if searched_device is None:
        return None

    return __Device_to_GetDeviceModel(searched_device)

def delete_device_by_id(db: Session, id: int):
    try:
        db.query(device.Device).filter(device.Device.id == id).delete()
        db.commit()
        return
    except Exception as e:
        raise e

def __Device_to_GetDeviceModel(device: device.Device) -> GetDeviceModel:

    return GetDeviceModel(id=device.id, device_name=device.device_name, username=device.username, created_at=device.created_at, updated_at=device.updated_at, deleted_at=device.deleted_at)
