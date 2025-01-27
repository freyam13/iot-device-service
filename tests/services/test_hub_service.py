import pytest

from src.models.device import DeviceType, SwitchState


def test_create_hub(hub_service) -> None:
    hub = hub_service.create_hub("Test Hub")

    assert hub.model_dump() == {
        "id": hub.id,
        "name": "Test Hub",
        "dwelling_id": None,
        "paired_device_ids": [],
    }


def test_pair_device(hub_service, device_service) -> None:
    hub = hub_service.create_hub("Test Hub")
    device = device_service.create_device(
        "Test Switch", DeviceType.SWITCH, SwitchState(is_on=False)
    )

    updated_hub = hub_service.pair_device(hub.id, device.id)
    updated_device = device_service.get_device(device.id)

    assert device.id in updated_hub.paired_device_ids
    assert updated_device.paired_hub_id == hub.id


def test_pair_already_paired_device(hub_service, device_service) -> None:
    hub_one = hub_service.create_hub("Hub 1")
    hub_two = hub_service.create_hub("Hub 2")
    device = device_service.create_device(
        "Test Switch", DeviceType.SWITCH, SwitchState(is_on=False)
    )

    hub_service.pair_device(hub_one.id, device.id)

    with pytest.raises(ValueError, match="Device .* is already paired to hub"):
        hub_service.pair_device(hub_two.id, device.id)


def test_get_device_state(hub_service, device_service) -> None:
    hub = hub_service.create_hub("Test Hub")
    device = device_service.create_device(
        "Test Switch", DeviceType.SWITCH, SwitchState(is_on=False)
    )

    hub_service.pair_device(hub.id, device.id)

    device_state = hub_service.get_device_state(hub.id, device.id)

    assert device_state.model_dump() == device.model_dump()


def test_list_devices(hub_service, device_service) -> None:
    hub = hub_service.create_hub("Test Hub")
    device_one = device_service.create_device(
        "Switch 1", DeviceType.SWITCH, SwitchState(is_on=False)
    )
    device_two = device_service.create_device(
        "Switch 2", DeviceType.SWITCH, SwitchState(is_on=True)
    )

    hub_service.pair_device(hub.id, device_one.id)
    hub_service.pair_device(hub.id, device_two.id)

    devices = hub_service.list_devices(hub.id)

    assert len(devices) == 2
    assert {d.id for d in devices} == {device_one.id, device_two.id}


def test_remove_device(hub_service, device_service) -> None:
    hub = hub_service.create_hub("Test Hub")
    device = device_service.create_device(
        "Test Switch", DeviceType.SWITCH, SwitchState(is_on=False)
    )

    hub_service.pair_device(hub.id, device.id)

    updated_hub = hub_service.remove_device(hub.id, device.id)
    updated_device = device_service.get_device(device.id)

    assert not updated_hub.paired_device_ids
    assert updated_device.paired_hub_id is None


def test_pair_nonexistent_device(hub_service) -> None:
    hub = hub_service.create_hub("Test Hub")

    with pytest.raises(ValueError, match="Device .* not found"):
        hub_service.pair_device(hub.id, "nonexistent-device")


def test_pair_to_nonexistent_hub(hub_service, device_service) -> None:
    device = device_service.create_device(
        "Test Device", DeviceType.SWITCH, SwitchState(is_on=False)
    )

    with pytest.raises(ValueError, match="Hub .* not found"):
        hub_service.pair_device("nonexistent-hub", device.id)
