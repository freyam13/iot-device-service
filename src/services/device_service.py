from typing import List, Optional
from uuid import uuid4

from src.models.device import Device, DeviceState, DeviceType
from src.repository.base import DB


class DeviceService:
    """
    Service for managing IoT Devices and their states.
    """

    def __init__(self, device_store: DB[Device]) -> None:
        """
        Initialize the Device service.

        Arguments:
            device_store: storage for Device entities
        """
        self._store = device_store

    def create_device(
        self, name: str, device_type: DeviceType, initial_state: DeviceState
    ) -> Device:
        """
        Create a new Device.

        Arguments:
            name: name of the Device
            device_type: type of device (switch, dimmer, etc.)
            initial_state: initial state configuration for the Device

        Returns:
            newly created Device
        """
        device = Device(
            id=str(uuid4()),
            name=name,
            type=device_type,
            state=initial_state,
        )
        return self._store.create(device.id, device)

    def delete_device(self, device_id: str) -> None:
        """
        Delete an unpaired Device.

        Arguments:
            device_id: identifier of the Device to delete

        Raises:
            ValueError: if Device not found or is currently paired
        """
        device = self._store.get(device_id)

        if not device:
            raise ValueError(f"Device {device_id} not found")

        if device.paired_hub_id:
            raise ValueError(f"Cannot delete device {device_id} while paired to a hub")

        self._store.delete(device_id)

    def get_device(self, device_id: str) -> Optional[Device]:
        """
        Get a Device by its identifier along with its state/metadata.

        Arguments:
            device_id: identifier of the Device to retrieve

        Returns:
            Device if found, None otherwise
        """
        return self._store.get(device_id)

    def modify_device_state(self, device_id: str, new_state: DeviceState) -> Device:
        """
        Update a Device's state.

        Arguments:
            device_id: identifier of the Device to update
            new_state: new state configuration for the Device

        Returns:
            updated Device

        Raises:
            ValueError: if Device not found
        """
        device = self._store.get(device_id)

        if not device:
            raise ValueError(f"Device {device_id} not found")

        if not isinstance(new_state, type(device.state)):
            raise ValueError(f"Cannot apply {new_state} to device type of {device.type}")

        device.state = new_state

        return self._store.update(device_id, device)

    def list_devices(self) -> List[Device]:
        """
        List all Devices.

        Returns:
            list of all Devices in the system
        """
        return self._store.list()
