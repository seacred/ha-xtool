"""CPU temperature: milli-degrees on the F2 Ultra UV, degrees on the M1 Ultra.

``/v1/device/runtime-infos`` reported ``cpuTemp: 43565`` on an F2 Ultra
UV (40.130.021.00.ht2) and ``cpuTemp: 43`` on an M1 Ultra
(40.41.018.2020.01.ht4); both are about 43 °C.
"""

from __future__ import annotations

import pytest

from custom_components.xtool.protocols.base import XtoolDeviceState


@pytest.mark.parametrize("cpu_temp", [43565, 43])
async def test_cpu_temperature(cpu_temp: int) -> None:
    from custom_components.xtool.protocols.ws_v2.protocol import WSV2Protocol

    async def request(url, method="GET", params=None, data=None, **kwargs):
        if url == "/v1/device/runtime-infos":
            return {"cpuTemp": cpu_temp, "curMode": {"mode": "P_IDLE"}}
        return {}

    proto = WSV2Protocol("192.0.2.10")
    proto._connected = True
    proto.request = request
    state = XtoolDeviceState()
    await proto.poll_state(state)
    assert state.cpu_temp == 43
