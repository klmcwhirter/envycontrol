

import envycontrol
from envycontrol import get_igpu_bus_pci_bus


def test_get_igpu_bus_pci_bus_should_return_formatted(monkeypatch):
    def mockreturn():
        return [
            '0000:00:02.0  Intel '
        ]

    monkeypatch.setattr(envycontrol, "get_lspci_lines", mockreturn)

    id = get_igpu_bus_pci_bus()

    assert 'PCI:0:2:0' == id
