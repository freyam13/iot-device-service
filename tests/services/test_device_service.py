import pytest

from src.models.device import (
    DeviceType,
    DimmerState,
    LockState,
    Mode,
    SwitchState,
    ThermostatState,
)


def test_create_device(device_service) -> None:
    device = device_service.create_device(
        "Test Switch", DeviceType.SWITCH, SwitchState(is_on=False)
    )

    assert device.name == "Test Switch"
    assert device.type == DeviceType.SWITCH
    assert isinstance(device.state, SwitchState)
    assert not device.state.is_on


def test_delete_device(device_service) -> None:
    device = device_service.create_device(
        "Test Switch", DeviceType.SWITCH, SwitchState(is_on=False)
    )
    device_service.delete_device(device.id)

    assert device_service.get_device(device.id) is None


def test_delete_paired_device(device_service) -> None:
    device = device_service.create_device(
        "Test Switch", DeviceType.SWITCH, SwitchState(is_on=False)
    )
    device.paired_hub_id = "test_hub"

    with pytest.raises(ValueError):
        device_service.delete_device(device.id)


def test_modify_device_state(device_service) -> None:
    device = device_service.create_device(
        "Test Switch", DeviceType.SWITCH, SwitchState(is_on=False)
    )
    updated_device = device_service.modify_device_state(
        device.id, SwitchState(is_on=True)
    )

    assert updated_device.state.is_on


def test_create_dimmer(device_service) -> None:
    device = device_service.create_device(
        "Test Dimmer", DeviceType.DIMMER, DimmerState(brightness=50, is_on=True)
    )

    assert device.model_dump() == {
        "id": device.id,
        "name": "Test Dimmer",
        "type": DeviceType.DIMMER,
        "state": {"brightness": 50, "is_on": True},
        "paired_hub_id": None,
    }


def test_create_lock(device_service) -> None:
    device = device_service.create_device(
        "Test Lock", DeviceType.LOCK, LockState(is_locked=True, pin_code="1234")
    )

    assert device.model_dump() == {
        "id": device.id,
        "name": "Test Lock",
        "type": DeviceType.LOCK,
        "state": {"is_locked": True, "pin_code": "1234"},
        "paired_hub_id": None,
    }


def test_create_thermostat(device_service) -> None:
    device = device_service.create_device(
        "Test Thermostat",
        DeviceType.THERMOSTAT,
        ThermostatState(current_temperature=68, mode=Mode.HEAT, target_temperature=72),
    )

    assert device.model_dump() == {
        "id": device.id,
        "name": "Test Thermostat",
        "type": DeviceType.THERMOSTAT,
        "state": {
            "current_temperature": 68.0,
            "mode": Mode.HEAT,
            "target_temperature": 72.0,
        },
        "paired_hub_id": None,
    }
