from pymetasploit3.msfrpc import MsfRpcClient

# Conectarse al servidor de Metasploit
client = MsfRpcClient('127.0.0.1', 55553, 'msf', 'msf')

# Obtener la lista de sesiones activas
sessions = client.sessions.list

# ID de sesión que deseas verificar
session_id = 1

# Buscar la sesión en la lista de sesiones activas
session = sessions.get(session_id)

if session:
    print(f"La sesión {session_id} está activa.")
    # Realizar otras operaciones con la sesión si es necesario
else:
    print(f"La sesión {session_id} no está activa.")



# ================================================



from msfrpc import MsfRpcClient

# Conectarse al servicio de Metasploit RPC
client = MsfRpcClient('password')

# Obtener una lista de sesiones
sessions = client.sessions.list

# Comprobar el estado de una sesión específica
session_id = 1  # ID de sesión deseado
session = sessions[session_id]

if session['busy']:
    print('La sesión está ocupada')
else:
    print('La sesión está disponible')
