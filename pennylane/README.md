# Accessing AQT resources from PennyLane

AQT computing resources can be accessed in [PennyLane](https://pennylane.ai/) using the [PennyLane-Qiskit](https://pypi.org/project/PennyLane-qiskit/) plugin and the [`qiskit.remote`](https://docs.pennylane.ai/projects/qiskit/en/latest/devices/remote.html) device.

The PennyLane circuit is translated into a Qiskit circuit and the Qiskit transpiler optimizes it to match the constraints of AQT computing resources.

## Getting started

This project's [`pyproject.toml`](./pyproject.toml) contains the tested set of dependencies.

Qiskit backends for AQT resources are retrieved from the Qiskit AQT provider:

```python
from qiskit_aqt_provider import AQTProvider

aqt_backend = AQTProvider("").get_backend("offline_simulator_no_noise")
 ```

The PennyLane device is then instantiated from the Qiskit backend:

```python
import pennylane as qml

dev = qml.device("qiskit.remote", backend=aqt_backend, wires=2, shots=200)
```

The PennyLane device can then be used to declare a quantum node:

```python
from math import pi

@qml.qnode(dev)
def circuit():
    qml.RX(pi, wires=0)
    return qml.expval(qml.PauliZ(0))

print(circuit())
```

## Examples

See the [examples](./examples) directory. Examples are written as Python unit tests to ease up their automatic verification.

Available examples:

  - Basic Bell states manipulation - [bell_states.py](./examples/bell_states.py)
  - QFT-based arithmetics, based on the eponymous [PennyLane demo](https://pennylane.ai/qml/demos/tutorial_qft_arithmetics) - [qft_arithmetics.py](./examples/qft_arithmetics.py)
