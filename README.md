# Smart Home Device Management System

## Overview

A robust Python-based system for managing smart home devices and their interactions. This project demonstrates clean architecture, domain-driven design, and modern Python development practices in implementing a device management solution for smart homes.

The system provides comprehensive management of:
- smart home hubs and devices
- device pairing and state management
- dwelling (home/building) management
- occupancy tracking
- device state monitoring and control

## Key Features

- **Device Management**
  - support for multiple device types (switches, dimmers, locks, thermostats)
  - device creation, deletion, and state management
  - type-safe state updates
  - comprehensive device information tracking

- **Hub Management**
  - device pairing and unpairing
  - state monitoring
  - device listing and status reporting
  - relationship management between hubs and devices

- **Dwelling Management**
  - occupancy tracking
  - hub installation and management
  - multi-dwelling support
  - dwelling listing and status reporting

## Technical Highlights

- clean architecture principles
- domain-driven design
- type safety with Pydantic
- comprehensive test coverage
- modular and extensible design
- in-memory storage with easy persistence pathway

## Setup

1. Install dependencies:
```bash
# Install pipenv if not already installed
pip install pipenv

# Install project dependencies
pipenv install --dev
```

2. Run tests:
```bash
pipenv run pytest
```

## Project Structure

```
src/
├── models/
│   ├── device.py                # Device and state models
│   ├── hub.py                   # Hub model
│   └── dwelling.py              # Dwelling model
├── services/
│   ├── device_service.py        # Device management
│   ├── hub_service.py           # Hub and pairing logic
│   └── dwelling_service.py      # Dwelling management
└── repository/
    └── memory_store.py          # in-memory storage

tests/
├── services/
│   ├── test_device_service.py   # Device management tests
│   ├── test_hub_service.py      # Hub and pairing tests
│   ├── test_dwelling_service.py # Dwelling management tests
└── conftest.py                  # test fixtures
```

## Implementation Details

1. **Storage Layer**
   - implements a flexible in-memory storage system
   - designed for easy transition to persistent storage
   - separate store instances for each entity type
   - thread-safe operations

2. **Device State Management**
   - immutable state objects using Pydantic
   - type-safe state updates
   - comprehensive validation
   - support for multiple device types

3. **Hub Management**
   - robust device pairing system
   - bi-directional relationship tracking
   - safety checks for device deletion
   - state synchronization

4. **Dwelling Management**
   - occupancy state tracking
   - hub installation management
   - relationship maintenance
   - status reporting

## Example Usage

The test suite provides comprehensive examples of system usage:

1. **Device Management** (`test_device_service.py`):
```python
# Create a switch device
switch = device_service.create_device("switch", "Living Room Light")
# Modify device state
device_service.modify_device(switch.id, {"power": "ON"})
```

2. **Hub Management** (`test_hub_service.py`):
```python
# Create and pair a device
hub = hub_service.create_hub("Main Hub")
hub_service.pair_device(hub.id, device.id)
```

3. **Dwelling Management** (`test_dwelling_service.py`):
```python
# Create and manage dwelling
dwelling = dwelling_service.create_dwelling("123 Main St")
dwelling_service.set_occupied(dwelling.id)
```

## Design Goals

- **Maintainability**: clean, well-documented code following SOLID principles
- **Extensibility**: easy to add new device types and features
- **Reliability**: comprehensive error handling and validation
- **Testability**: high test coverage and easy-to-test components
- **Type Safety**: strong typing throughout the codebase

## Future Enhancements

- persistent storage implementation
- REST API layer
- real-time device updates
- authentication and authorization
- device grouping and scenes
- advanced automation rules
