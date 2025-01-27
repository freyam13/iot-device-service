import pytest


def test_create_dwelling(dwelling_service) -> None:
    dwelling = dwelling_service.create_dwelling("Test Dwelling")

    assert dwelling.model_dump() == {
        "id": dwelling.id,
        "name": "Test Dwelling",
        "is_occupied": False,
        "hub_ids": [],
    }


def test_set_occupied_status(dwelling_service) -> None:
    dwelling = dwelling_service.create_dwelling("Test Dwelling")

    # test occupied
    updated = dwelling_service.set_occupied_status(dwelling.id, True)

    assert updated.model_dump() == {
        "id": dwelling.id,
        "name": "Test Dwelling",
        "is_occupied": True,
        "hub_ids": [],
    }

    # test vacant
    updated = dwelling_service.set_occupied_status(dwelling.id, False)

    assert updated.model_dump() == {
        "id": dwelling.id,
        "name": "Test Dwelling",
        "is_occupied": False,
        "hub_ids": [],
    }


def test_install_hub(dwelling_service, hub_service) -> None:
    dwelling = dwelling_service.create_dwelling("Test Dwelling")
    hub = hub_service.create_hub("Living Room Hub")

    updated_dwelling = dwelling_service.install_hub(dwelling.id, hub.id)

    assert hub.id in updated_dwelling.hub_ids


def test_install_already_installed_hub(dwelling_service, hub_service) -> None:
    dwelling_one = dwelling_service.create_dwelling("Dwelling 1")
    dwelling_two = dwelling_service.create_dwelling("Dwelling 2")
    hub = hub_service.create_hub("Living Room Hub")

    dwelling_service.install_hub(dwelling_one.id, hub.id)

    with pytest.raises(ValueError, match="Hub .* is already installed in dwelling"):
        dwelling_service.install_hub(dwelling_two.id, hub.id)


def test_list_dwellings(dwelling_service) -> None:
    dwelling_one = dwelling_service.create_dwelling("Dwelling 1")
    dwelling_two = dwelling_service.create_dwelling("Dwelling 2")

    dwellings = dwelling_service.list_dwellings()
    dwelling_dicts = [d.model_dump() for d in dwellings]

    assert len(dwellings) == 2
    assert dwelling_one.model_dump() in dwelling_dicts
    assert dwelling_two.model_dump() in dwelling_dicts


def test_install_hub_to_nonexistent_dwelling(dwelling_service, hub_service) -> None:
    hub = hub_service.create_hub("Test Hub")

    with pytest.raises(ValueError, match="Dwelling .* not found"):
        dwelling_service.install_hub("nonexistent-dwelling", hub.id)


def test_install_nonexistent_hub(dwelling_service) -> None:
    dwelling = dwelling_service.create_dwelling("Test Dwelling")

    with pytest.raises(ValueError, match="Hub .* not found"):
        dwelling_service.install_hub(dwelling.id, "nonexistent-hub")
