# MIT License - Usar misma licencia que el repositorio
"""
Backend IBM Quantum (stub de integración).

Proporciona la clase IBMQBackend para enviar circuitos cuánticos
al servicio IBM Quantum. Por seguridad, no se incluyen claves de API.

Para habilitar la integración real:
1. Instalar: pip install qiskit qiskit-ibm-runtime
2. Obtener tu API key en https://quantum-computing.ibm.com/
3. Pasar la clave como variable de entorno IBM_QUANTUM_API_KEY
   o directamente en el método submit_circuit(circuit, api_key="TU_CLAVE").

ADVERTENCIA: Nunca incluir claves de API directamente en el código fuente.
"""


class IBMQBackend:
    """
    Cliente stub para IBM Quantum.

    En producción, esta clase encapsularía la autenticación y el envío
    de trabajos cuánticos a través de qiskit-ibm-runtime.
    """

    def __init__(self, backend_name="ibmq_qasm_simulator"):
        """
        Inicializa el backend de IBM Quantum.

        Parámetros
        ----------
        backend_name : str
            Nombre del backend de IBM Quantum a usar.
            Ejemplos: "ibmq_qasm_simulator", "ibmq_manila".
        """
        self.backend_name = backend_name

    def submit_circuit(self, circuit, api_key=None):
        """
        Envía un circuito cuántico a IBM Quantum para su ejecución.

        Parámetros
        ----------
        circuit : dict
            Representación del circuito cuántico (formato interno).
        api_key : str, opcional
            Clave de API de IBM Quantum. Si es None, se buscará en
            la variable de entorno IBM_QUANTUM_API_KEY.

        Lanza
        -----
        NotImplementedError
            Siempre, ya que es un stub de integración.

        Notas
        -----
        Para implementación real, usar qiskit-ibm-runtime:

            from qiskit_ibm_runtime import QiskitRuntimeService
            service = QiskitRuntimeService(channel="ibm_quantum", token=api_key)
            backend = service.backend(self.backend_name)
            # Convertir circuit a formato Qiskit y enviar...
        """
        raise NotImplementedError(
            "IBMQBackend.submit_circuit no está implementado. "
            "Instala qiskit e ibm-runtime y configura tu API key para usar "
            "hardware real de IBM Quantum."
        )
