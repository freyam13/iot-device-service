from fastapi import APIRouter, status, HTTPException, Depends

from src.models.device import Device
from src.services.device_service import DeviceService

router = APIRouter()


@router.post("/devices", response_model=Device, status_code=status.HTTP_201_CREATED)
async def create_device(device: Device, service: DeviceService = Depends(DeviceService)) -> Device:
    """
    Create a new device.

    Arguments:
        device: the Device to be created
        service: dependency injection

    Returns:
        device: newly created Device

    Raises:
        HTTPException: if Device creation fails
    """
    try:
        return service.create_device(device.name, device.type, device.state)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
