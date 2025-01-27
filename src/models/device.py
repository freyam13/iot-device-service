from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict


class DeviceType(Enum):
    CAMERA = "camera"
    DIMMER = "dimmer"
    LOCK = "lock"
    SWITCH = "switch"
    THERMOSTAT = "thermostat"


class Mode(Enum):
    OFF = "off"
    HEAT = "heat"
    COOL = "cool"


class DeviceState(BaseModel):
    """
    Base class for device states for all device-specific state implementations,
    ensuring type safety and common interface across different device types.
    """

    model_config = ConfigDict(from_attributes=True)

class CameraState(DeviceState):
    is_recording: bool = False
    resolution: str = "1080p"

class SwitchState(DeviceState):
    is_on: bool = False


class DimmerState(DeviceState):
    brightness: int = 0
    is_on: bool = False


class LockState(DeviceState):
    is_locked: bool = True
    pin_code: Optional[str] = None


class ThermostatState(DeviceState):
    mode: Mode = Mode.OFF
    current_temperature: float = 78.0
    target_temperature: float = 78.0


class Device(BaseModel):
    id: str
    name: str
    type: DeviceType
    state: Union[SwitchState, DimmerState, LockState, ThermostatState]
    paired_hub_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
