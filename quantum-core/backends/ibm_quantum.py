# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Backend IBM Quantum
====================
Clase stub para conexión con IBM Quantum (hardware real o simulador en la nube).

IMPORTANTE: Este módulo no incluye ninguna clave API ni habilita hardware real
por defecto. Para usar IBM Quantum es necesario:
1. Obtener una cuenta en https://quantum.ibm.com
2. Instalar qiskit-ibm-runtime: pip install qiskit-ibm-runtime
3. Configurar el token mediante QiskitRuntimeService.save_account()

No almacenar claves API en el código fuente ni en el control de versiones.
"""


class IBMQBackend:
    """
    Backend para enviar circuitos a IBM Quantum (stub).

    Esta clase define la interfaz para interactuar con IBM Quantum mediante
    qiskit-ibm-runtime. La implementación actual lanza NotImplementedError
    en todos los métodos que requieren conexión real para evitar el uso
    accidental de hardware cuántico o credenciales no configuradas.

    Uso previsto (una vez configurado qiskit-ibm-runtime):
    -------------------------------------------------------
    >>> from qiskit_ibm_runtime import QiskitRuntimeService
    >>> # service = QiskitRuntimeService(channel="ibm_quantum", token="TU_TOKEN")
    >>> backend = IBMQBackend(backend_name="ibmq_qasm_simulator")
    >>> resultado = backend.submit_circuit(circuito)

    Atributos
    ---------
    backend_name : str
        Nombre del backend de IBM Quantum a usar.
    max_shots : int
        Número máximo de disparos (mediciones) por circuito.
    timeout : int
        Tiempo máximo de espera en segundos para resultados.
    """

    def __init__(self, backend_name="ibmq_qasm_simulator", max_shots=1024, timeout=300):
        """
        Inicializa el backend IBM Quantum sin establecer conexión.

        Parámetros
        ----------
        backend_name : str
            Nombre del backend de IBM Quantum. Por defecto el simulador QASM.
        max_shots : int
            Número de disparos para la ejecución del circuito.
        timeout : int
            Tiempo máximo de espera en segundos.
        """
        self.backend_name = backend_name
        self.max_shots = max_shots
        self.timeout = timeout
        self._service = None  # QiskitRuntimeService (no configurado por defecto)

    def connect(self, token=None):
        """
        Establece conexión con IBM Quantum usando el token proporcionado.

        Parámetros
        ----------
        token : str o None
            Token de IBM Quantum. Si es None, intenta cargar la configuración
            guardada localmente con QiskitRuntimeService.saved_account().

        Lanza
        -----
        NotImplementedError
            Siempre, hasta que se instale qiskit-ibm-runtime y se configure
            el token correctamente.
        """
        raise NotImplementedError(
            "IBMQBackend.connect() no implementado. "
            "Para habilitar: instala qiskit-ibm-runtime y configura tu token de IBM Quantum. "
            "Consulta quantum-core/docs/api_reference.md para instrucciones."
        )

    def submit_circuit(self, circuit):
        """
        Envía un circuito cuántico a IBM Quantum para su ejecución.

        Parámetros
        ----------
        circuit : dict
            Representación del circuito (formato interno de quantum-core) o
            objeto QuantumCircuit de Qiskit.

        Retorna
        -------
        dict
            Resultados de la ejecución con conteos de medición.

        Lanza
        -----
        NotImplementedError
            Siempre. Este método requiere configuración de IBM Quantum.
        """
        raise NotImplementedError(
            "IBMQBackend.submit_circuit() no implementado. "
            "Usa LocalSimulator para pruebas locales. "
            "Para IBM Quantum real: configura qiskit-ibm-runtime con tu cuenta."
        )

    def get_available_backends(self):
        """
        Obtiene la lista de backends disponibles en IBM Quantum.

        Lanza
        -----
        NotImplementedError
            Siempre. Requiere conexión activa con IBM Quantum.
        """
        raise NotImplementedError(
            "IBMQBackend.get_available_backends() no implementado. "
            "Requiere conexión a IBM Quantum."
        )

    def __repr__(self):
        return (
            f"IBMQBackend(backend_name={self.backend_name!r}, "
            f"max_shots={self.max_shots}, timeout={self.timeout})"
        )
