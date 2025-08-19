from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.schemas.device import DeviceAuthValidation, DeviceCreationModel, ReturnNewDeviceModel, GetDeviceModel
from app.dependencies import get_db
from app.services.user_service import validate_device_auth, create_device, list_device, get_device_by_id, delete_device_by_id
from app.dependencies import logger
from fastapi.encoders import jsonable_encoder
from typing import List

router = APIRouter(prefix="/broker", tags=["broker"])


@router.post("/auth", response_model=bool)
def device_broker_auth(device: DeviceAuthValidation, db: Session = Depends(get_db)):

    result = validate_device_auth(db, device)


    if not result:
        return JSONResponse(status_code=403, content={"Ok": False, "Error": "Authentication failed."})

    return JSONResponse(status_code=200, content={"Ok": True, "Error": ""})

@router.post("/", response_model=ReturnNewDeviceModel)
def device_creation(device: DeviceCreationModel, db: Session = Depends(get_db)):

    try:
        created_device = create_device(db, device)
        return JSONResponse(content=jsonable_encoder(created_device), status_code=201)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Failed to create device : {e}")

@router.get("/", response_model=List[GetDeviceModel])
def list_devices(db: Session = Depends(get_db)):

    try:
        return JSONResponse(content=jsonable_encoder(list_device(db)), status_code=200)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"Failed to create device : {e}")

@router.get("/{id}", response_model=GetDeviceModel)
def get_device(id: int, db: Session = Depends(get_db)):

    searched_device = get_device_by_id(db, id)

    if searched_device is None:
        raise HTTPException(404, detail=f"Device with id {id} doesn't exist.")

    return JSONResponse(content=jsonable_encoder(searched_device), status_code=200)

@router.delete("/{id}")
def delete_device(id: int, db: Session = Depends(get_db)):

    try:
        delete_device_by_id(db, id)
        return Response(status_code=204)
    except:
        raise HTTPException(status_code=500, detail=f"Failed to delete device with id {id}")