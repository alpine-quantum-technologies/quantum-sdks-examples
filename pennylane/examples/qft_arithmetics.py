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
from pennylane.measurements import SampleMP
from qiskit_aqt_provider import AQTProvider

# Retrieve a noiseless offline simulator resource from the Qiskit AQT provider.
# Fix the underlying simulator's random generation seed such that the examples
# are exactly reproducible.
qiskit_backend = AQTProvider("").get_backend("offline_simulator_no_noise")
qiskit_backend.options.with_progress_bar = False
qiskit_backend.simulator.options.seed_simulator = 12345


def example_qft_sum() -> None:
    """Basic sum arithmetic with the quantum Fourier transform.

    Based on:
    https://pennylane.ai/qml/demos/tutorial_qft_arithmetics
    """
    n_wires = 4
    wires = list(range(n_wires))
    dev = qml.device("qiskit.remote", backend=qiskit_backend, wires=n_wires, shots=1)

    def add_k_fourier(k: float, wires: list[int]) -> None:
        for j in range(len(wires)):
            qml.RZ(k * pi / (2**j), wires=wires[j])

    @qml.qnode(dev)
    def encode(m: int) -> SampleMP:
        """Encode the integer m on the computational basis."""
        qml.BasisEmbedding(m, wires=wires)
        return qml.sample()

    @qml.qnode(dev)
    def sum(m: int, k: int) -> SampleMP:
        """QFT-based sum of a qubit with a register.

        Implements: sum(k)|m> = |m+k>
        where |m> is the representation of integer m.
        """
        qml.BasisEmbedding(m, wires=wires)
        qml.QFT(wires=wires)
        add_k_fourier(k, wires)
        qml.adjoint(qml.QFT)(wires=wires)

        return qml.sample()

    assert (encode(3) == [0, 0, 1, 1]).all()
    assert (encode(4) == [0, 1, 0, 0]).all()

    assert (sum(3, 4) == [0, 1, 1, 1]).all()
