import pytest

from src.models.device import Device
from src.models.dwelling import Dwelling
from src.models.hub import Hub
from src.repository.memory_store import PostgresStore
from src.services.device_service import DeviceService
from src.services.dwelling_service import DwellingService
from src.services.hub_service import HubService


@pytest.fixture
def device_store():
    return PostgresStore[Device]()


@pytest.fixture
def hub_store():
    return PostgresStore[Hub]()


@pytest.fixture
def dwelling_store():
    return PostgresStore[Dwelling]()


@pytest.fixture
def device_service(device_store):
    return DeviceService(device_store)


@pytest.fixture
def hub_service(hub_store, device_store):
    return HubService(hub_store, device_store)


@pytest.fixture
def dwelling_service(dwelling_store, hub_store):
    return DwellingService(dwelling_store, hub_store)
