from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.exceptions.database import EntityNotFound
from app.schemas.device import DeviceAuthValidation, DeviceCreationModel, ReturnNewDeviceModel, GetDeviceModel, IsSuperUser
from app.schemas.acl import NewAclModel, ReturnNewAclModel, GetAclModel, AclCheck
from app.dependencies import get_db
from app.services.user_service import validate_device_auth, create_device, list_device, get_device_by_id, delete_device_by_id, is_super_user
from app.services.acl_service import create_acl, get_acl, get_acls, remove_acl, validate_acl
from app.dependencies import logger
from fastapi.encoders import jsonable_encoder
from typing import List

router = APIRouter(prefix="/broker", tags=["broker"])

@router.post("/device/auth")
def device_broker_auth(device: DeviceAuthValidation, db: Session = Depends(get_db)):

    result = validate_device_auth(db, device)


    if not result:
        return JSONResponse(status_code=403, content={"Ok": False, "Error": "Authentication failed."})

    return JSONResponse(status_code=200, content={"Ok": True, "Error": ""})

@router.post("/device/verify_acl")
def device_broker_verify_acl(check: AclCheck, db: Session = Depends(get_db)):

    if validate_acl(db, check):
        return JSONResponse(status_code=200, content=jsonable_encoder({"Ok": True, "Error": ""}))

    return JSONResponse(status_code=200, content=jsonable_encoder({"Ok": False, "Error": "Device doesn't have permission"}))

@router.post("/device", response_model=ReturnNewDeviceModel)
def device_creation(device: DeviceCreationModel, db: Session = Depends(get_db)):

    try:
        created_device = create_device(db, device)
        return JSONResponse(content=jsonable_encoder(created_device), status_code=201)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Failed to create device : {e}")

@router.get("/device", response_model=List[GetDeviceModel])
def list_devices(db: Session = Depends(get_db)):

    try:
        return JSONResponse(content=jsonable_encoder(list_device(db)), status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Failed to create device : {e}")

@router.get("/device/{id}", response_model=GetDeviceModel)
def get_device(id: int, db: Session = Depends(get_db)):

    searched_device = get_device_by_id(db, id)

    if searched_device is None:
        raise HTTPException(404, detail=f"Device with id {id} doesn't exist.")

    return JSONResponse(content=jsonable_encoder(searched_device), status_code=200)

@router.delete("/device/{id}")
def delete_device(id: int, db: Session = Depends(get_db)):

    try:
        delete_device_by_id(db, id)
        return Response(status_code=204)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=jsonable_encoder(e.details))
    except:
        raise HTTPException(status_code=500, detail=f"Failed to delete device with id {id}")

@router.post("/device/super_user")
def broker_is_super_user(super_user: IsSuperUser, db: Session = Depends(get_db)):

    if is_super_user(db, super_user.username):

        return JSONResponse(status_code=200, content=jsonable_encoder({"Ok": True, "Error": ""}))

    return JSONResponse(status_code=400, content=jsonable_encoder({"Ok": False, "Error": "User is not a super user"}))

@router.post("/device/{id}/acl", response_model=ReturnNewAclModel)
def new_acl(id: int, new_acl: NewAclModel, db: Session = Depends(get_db)):

    try:
        result = create_acl(db, id, new_acl)
        return JSONResponse(status_code=201, content=jsonable_encoder(result))
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=f"Device with id {id} not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create acl for the device with id {id}: {e}")

@router.get("/device/{device_id}/acl/{acl_id}", response_model=GetAclModel)
def get_acl_by_id(device_id: int, acl_id: int, db: Session = Depends(get_db)):

    try:
        return JSONResponse(status_code=200, content=jsonable_encoder(get_acl(db, device_id, acl_id)))
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=jsonable_encoder(e.details))
    except Exception as e:
        raise HTTPException(status_code=500, detail=jsonable_encoder(e))

@router.get("/device/{device_id}/acls", response_model=List[GetAclModel])
def get_acls_of_device(device_id: int, db: Session = Depends(get_db)):

    try:
        return JSONResponse(status_code=200, content=jsonable_encoder((get_acls(db, device_id))))
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=jsonable_encoder(e.details))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=jsonable_encoder(e))

@router.delete("/device/{device_id}/acl/{acl_id}")
def delete_acl(device_id: int, acl_id: int, db: Session = Depends(get_db)):

    try:
        remove_acl(db, device_id, acl_id)
        return Response(status_code=204)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=jsonable_encoder(e.details))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=jsonable_encoder(e))
