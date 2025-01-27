from typing import List
from uuid import uuid4

from src.models.device import Device
from src.models.hub import Hub
from src.repository.base import DB


class HubService:
    """
    Service for managing Hubs and their device associations.
    """

    def __init__(
        self, hub_store: DB[Hub], device_store: DB[Device]
    ) -> None:
        """
        Initialize the Hub service.

        Arguments:
            hub_store: storage for Hub entities
            device_store: storage for Device entities
        """
        self._hub_store = hub_store
        self._device_store = device_store

    def create_hub(self, name: str) -> Hub:
        """
        Create a new Hub.

        Arguments:
            name: name of the Hub to create

        Returns:
            newly created Hub
        """
        hub = Hub(id=str(uuid4()), name=name)

        return self._hub_store.create(hub.id, hub)

    def pair_device(self, hub_id: str, device_id: str) -> Hub:
        """
        Pair a Device with a Hub.

        Arguments:
            hub_id: identifier of the Hub
            device_id: identifier of the Device to pair

        Returns:
            updated Hub with paired Device

        Raises:
            ValueError: if Hub or Device not found, or Device already paired
        """
        hub = self._hub_store.get(hub_id)
        device = self._device_store.get(device_id)

        if not hub:
            raise ValueError(f"Hub {hub_id} not found")

        if not device:
            raise ValueError(f"Device {device_id} not found")

        if device.paired_hub_id:
            raise ValueError(
                f"Device {device_id} is already paired to hub {device.paired_hub_id}"
            )

        hub.paired_device_ids.append(device_id)
        device.paired_hub_id = hub_id

        self._device_store.update(device_id, device)

        return self._hub_store.update(hub_id, hub)

    def get_device_state(self, hub_id: str, device_id: str) -> Device:
        """
        Get the current state of a Device through its Hub.

        Arguments:
            hub_id: identifier of the Hub
            device_id: identifier of the Device to query

        Returns:
            Device with its current state

        Raises:
            ValueError: if Hub or Device not found, or Device not paired with Hub
        """
        hub = self._hub_store.get(hub_id)
        device = self._device_store.get(device_id)

        if not hub:
            raise ValueError(f"Hub {hub_id} not found")

        if not device:
            raise ValueError(f"Device {device_id} not found")

        if device_id not in hub.paired_device_ids:
            raise ValueError(f"Device {device_id} is not paired with hub {hub_id}")

        return device

    def list_devices(self, hub_id: str) -> List[Device]:
        """
        List all Devices paired with a Hub.

        Arguments:
            hub_id: identifier of the Hub to query

        Returns:
            list of Devices paired with the Hub

        Raises:
            ValueError: if Hub not found
        """
        hub = self._hub_store.get(hub_id)

        if not hub:
            raise ValueError(f"Hub {hub_id} not found")

        return [
            self._device_store.get(device_id) for device_id in hub.paired_device_ids
        ]

    def remove_device(self, hub_id: str, device_id: str) -> Hub:
        """
        Remove a Device from a Hub.

        Arguments:
            hub_id: identifier of the Hub
            device_id: identifier of the Device to remove

        Returns:
            updated Hub with Device removed

        Raises:
            ValueError: if Hub or Device not found, or Device not paired with Hub
        """
        hub = self._hub_store.get(hub_id)
        device = self._device_store.get(device_id)

        if not hub:
            raise ValueError(f"Hub {hub_id} not found")

        if not device:
            raise ValueError(f"Device {device_id} not found")

        if device_id not in hub.paired_device_ids:
            raise ValueError(f"Device {device_id} is not paired with hub {hub_id}")

        hub.paired_device_ids.remove(device_id)
        device.paired_hub_id = None

        self._device_store.update(device_id, device)

        return self._hub_store.update(hub_id, hub)
