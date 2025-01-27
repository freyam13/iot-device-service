from typing import List
from uuid import uuid4

from src.models.dwelling import Dwelling
from src.models.hub import Hub
from src.repository.base import DB


class DwellingService:
    """
    Service for managing Dwellings and their hub installations.
    """

    def __init__(
        self, dwelling_store: DB[Dwelling], hub_store: DB[Hub]
    ) -> None:
        """
        Initialize the Dwelling service.

        Arguments:
            dwelling_store: storage for Dwelling entities.
            hub_store: storage for Hub entities.
        """
        self._dwelling_store = dwelling_store
        self._hub_store = hub_store

    def create_dwelling(self, name: str) -> Dwelling:
        """
        Create a new Dwelling.

        Arguments:
            name: name of the Dwelling

        Returns:
            newly created Dwelling
        """
        dwelling = Dwelling(id=str(uuid4()), name=name)
        return self._dwelling_store.create(dwelling.id, dwelling)

    def set_occupied_status(self, dwelling_id: str, is_occupied: bool) -> Dwelling:
        """
        Update Dwelling occupancy status.

        Arguments:
            dwelling_id: identifier of the dwelling
            is_occupied: new occupancy status

        Returns:
            updated Dwelling

        Raises:
            ValueError: if Dwelling not found
        """
        dwelling = self._dwelling_store.get(dwelling_id)

        if not dwelling:
            raise ValueError(f"Dwelling {dwelling_id} not found")

        dwelling.is_occupied = is_occupied

        return self._dwelling_store.update(dwelling_id, dwelling)

    def install_hub(self, dwelling_id: str, hub_id: str) -> Dwelling:
        """
        Install a Hub in a Dwelling.

        Arguments:
            dwelling_id: identifier of the dwelling
            hub_id: identifier of the hub to install

        Returns:
            updated Dwelling with installed Hub.

        Raises:
            ValueError: if Dwelling or Hub not found, or Hub already installed.
        """
        dwelling = self._dwelling_store.get(dwelling_id)
        hub = self._hub_store.get(hub_id)

        if not dwelling:
            raise ValueError(f"Dwelling {dwelling_id} not found")

        if not hub:
            raise ValueError(f"Hub {hub_id} not found")

        if hub.dwelling_id:
            raise ValueError(
                f"Hub {hub_id} is already installed in dwelling {hub.dwelling_id}"
            )

        dwelling.hub_ids.append(hub_id)
        hub.dwelling_id = dwelling_id

        self._hub_store.update(hub_id, hub)

        return self._dwelling_store.update(dwelling_id, dwelling)

    def list_dwellings(self) -> List[Dwelling]:
        """
        List all Dwellings.

        Returns:
            list of all Dwellings in the system
        """
        return self._dwelling_store.list()
