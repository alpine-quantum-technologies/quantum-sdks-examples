# Copyright 2023 Alpine Quantum Technologies GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from math import pi

import pennylane as qml
from pennylane.qnode import CountsMP
from qiskit_aqt_provider import AQTProvider

# Retrieve a noiseless offline simulator resource from the Qiskit AQT provider.
# Fix the underlying simulator's random generation seed such that the examples
# are exactly reproducible.
qiskit_backend = AQTProvider("").get_backend("offline_simulator_no_noise")
qiskit_backend.options.with_progress_bar = False
qiskit_backend.simulator.options.seed_simulator = 12345


def example_bell_states() -> None:
    """Generate the |Ψ+> and |Φ+> Bell states and check their basic properties."""
    dev = qml.device("qiskit.remote", backend=qiskit_backend, wires=2, shots=200)

    @qml.qnode(dev)
    def phi_plus() -> CountsMP:
        """Create the Bell state (|00> + |11>)/√2."""
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()

    @qml.qnode(dev)
    def psi_plus() -> CountsMP:
        """Create the Bell state (|10> + |01>)/√2."""
        qml.RX(pi, wires=1)
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()

    phi = phi_plus()
    psi = psi_plus()

    assert phi == {"00": 103, "11": 97}
    assert psi == {"10": 103, "01": 97}
