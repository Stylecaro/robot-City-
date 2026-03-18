"""
Plantilla para el backend IBM Quantum (IBMQ) en Ciudad Robot.

Descripción:
    Clase de integración con el servicio IBM Quantum mediante la API de Qiskit.
    Por defecto NO se conecta a hardware real; requiere configuración explícita
    con una API key válida de IBM Quantum (https://quantum.ibm.com).

Configuración necesaria para uso real:
    1. Crear cuenta en https://quantum.ibm.com
    2. Obtener el token de API desde el perfil de usuario.
    3. Pasar el token en ``submit_circuit(circuit, api_key="TU_TOKEN")``
       o definir la variable de entorno ``IBMQ_API_KEY``.

    **IMPORTANTE**: No incluir claves de API en el código fuente ni en commits.

Dependencias opcionales:
    qiskit >= 1.0  (ver requirements.txt)
    qiskit-ibm-runtime >= 0.20

Uso de ejemplo (requiere Qiskit instalado)::

    backend = IBMQBackend(backend_name="ibm_brisbane")
    resultado = backend.submit_circuit(mi_circuito, api_key="TOKEN_SEGURO")
"""

# MIT License — Copyright (c) 2026 Ciudad Robot Team


class IBMQBackend:
    """Plantilla de integración con IBM Quantum.

    Proporciona la interfaz para enviar circuitos al hardware real de IBM Quantum.
    Actualmente lanza ``NotImplementedError`` para evitar ejecuciones accidentales
    en hardware real.

    Atributos:
        backend_name (str): Nombre del backend de IBM Quantum. Por defecto
            ``"ibm_brisbane"``.

    Ejemplo::

        >>> backend = IBMQBackend()
        >>> backend.backend_name
        'ibm_brisbane'
    """

    def __init__(self, backend_name="ibm_brisbane"):
        """Inicializa el backend IBMQ.

        Parámetros:
            backend_name (str): Nombre del procesador cuántico de IBM.
                Ejemplos: ``"ibm_brisbane"``, ``"ibm_kyoto"``, ``"simulator_mps"``.
        """
        self.backend_name = backend_name

    def submit_circuit(self, circuit, api_key=None):
        """Envía un circuito al backend IBM Quantum (no implementado).

        Parámetros:
            circuit: Circuito cuántico en formato Qiskit ``QuantumCircuit`` o
                representación dict del módulo quantum-core.
            api_key (str | None): Token de autenticación IBM Quantum. Si es None,
                intenta leer la variable de entorno ``IBMQ_API_KEY``.

        Lanza:
            NotImplementedError: Siempre. Esta es una plantilla que documenta
                la integración. Implementar con Qiskit para uso real.

        Pasos de implementación::

            # 1. Instalar dependencias:
            #    pip install qiskit qiskit-ibm-runtime
            #
            # 2. Autenticarse:
            #    from qiskit_ibm_runtime import QiskitRuntimeService
            #    service = QiskitRuntimeService(channel="ibm_quantum", token=api_key)
            #
            # 3. Obtener backend y ejecutar:
            #    backend = service.backend(self.backend_name)
            #    from qiskit_ibm_runtime import SamplerV2 as Sampler
            #    sampler = Sampler(backend)
            #    job = sampler.run([circuit])
            #    result = job.result()
            #    return result
        """
        raise NotImplementedError(
            "IBMQBackend.submit_circuit no está implementado. "
            "Consulta la documentación en quantum-core/docs/api_reference.md "
            "para instrucciones de integración con IBM Quantum."
        )
