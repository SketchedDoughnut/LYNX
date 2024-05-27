# this below code has been contributed to by chat gpt
import socket
# import time

_valid_ports = [
    11111,
    12111,
    11211,
    11121,
    11112,
    22111,
    12211,
    11221,
    11122,
    22222
]

# define all global vars
_HOST, _PORT = '', _valid_ports[0] # local_HOST
_main_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# override info
_ov_ports = []
_do_print = False





## FUNCTIONS - overrides, features
def override_ports(ports: list) -> None:
    ''' 
    Overrides what ports the client will attempt to connect to
    '''
    global _ov_ports
    _ov_ports = ports

# disable prints
def disable_print() -> None:
    '''
    Disables the client from printing messages
    '''
    global _do_print
    _do_print = False

# enable prints
def enable_print() -> None:
    '''
    Enables the client to print messages
    '''
    global _do_print
    _do_print = True

# function to handle printing
def pprint(msg: str) -> None:
    '''
    A function meant for filtering prints based on if it is enabled or disabled - This is meant for internal use
    '''
    if _do_print:
        print(msg)
    else:
        pass

# function to display current data
def get_data() -> dict:
    '''
    Returns data about the current client in the form of a dictionary
    '''
    return {
        'client info': {
            'ip': _HOST,
            'port': _PORT
        },
        'sillies': 'sillies :3'
    }





## FUNCTIONS - operations
# cycles port connection
def _cycle_port(client: socket.socket) -> socket.socket:
    '''
    An internal function used to cycle through the ports in _valid_ports to try and find a connection
    '''
    connected = False
    for port in _valid_ports:
        try:
            pprint(f'[PORT CYCLE] Client trying port: {port}')
            client.connect((_HOST, port))
            pprint(f'[PORT CYCLE] Client connected to: {port}')
            pprint('----------------------------------------------')
            connected = True
            break
        except IndexError:
            port = _valid_ports[0]
            pprint(f'[PORT CYCLE - RESET 1] Client resetting port to: {port}')
        except:
            try:
                pprint(f'[PORT CYCLE] Client port cycling: {port} -> {_valid_ports[_valid_ports.index(port) + 1]}')
            except IndexError:
                port = _valid_ports[0]
                pprint(f'[PORT CYCLE - RESET 2] Client resetting port to: {port}')
    if connected == True:
        return client, port
    else:
        pprint('[PORT CYCLE] the client can not find a open valid server port, exiting')
        exit()



# a function to fully recieve the message from server (to try and prevent loss)
# def full_recieve(client: socket.socket) -> str:
#     message_length = len(client.recv(1024).decode('utf-8'))
#     incoming_message = ''
#     local_length = 0
#     while local_length <= message_length:
#         incoming_message += client.recv(1024).decode('utf-8')
#         local_length = len(incoming_message)
#     return incoming_message

# a function for submitting username data to the server
def submit_username_data(message: str) -> str:
    '''
    Submits a username to the server, which the server will associate with your IP and port.
    Returns a message that confirms that the action has happened.
    '''
    # local override for package form
    client = _main_client
    # encoded_message = message.encode('utf-8')
    encoded_message = f'username {message}'.encode('utf-8') # added username prefix by default
    client.sendall(encoded_message)
    pprint(f"Sent:     {message}")
    incoming_data = client.recv(1024).decode('utf-8')
    pprint(f"Received: {incoming_data}")
    return incoming_data

# requests ip and port from server
def request_username_data(message: str) -> any:
    '''
    requests data associated with a username from the server, and either returns 'None' meaning you entered an invalid username, 
    or returns the IP and port of the user in a tuple.
    '''
    # local override for package form
    client = _main_client
    # encoded_message = message.encode('utf-8')
    encoded_message = f'request_by_user {message}'.encode('utf-8') # added request_by_user prefix by default
    client.sendall(encoded_message)
    pprint(f"Sent:     {message}")
    # incoming_data = full_recieve(client)
    incoming_data = client.recv(1024).decode('utf-8')
    pprint(f"Received: {incoming_data}")
    return incoming_data

# a general message sender
def general_send(message: str) -> str:
    '''
    A general tool function for sending messages to the recipient (server, other client, etc)
    '''
    # local override for package form
    client = _main_client
    encoded_message = message.encode('utf-8')
    client.sendall(encoded_message)
    pprint(f"Sent:     {message}")
    # incoming_data = full_recieve(client)
    incoming_data = client.recv(1024).decode('utf-8')
    pprint(f"Received: {incoming_data}")
    return incoming_data





# function for shutting down the client
def shutdown_client() -> bool:
    '''
    A function to shut down the client: returns a bool telling you whether it worked or not.
    '''
    global _main_client
    try:
        _main_client.close()
        pprint('[CLIENT SHUTDOWN] Shutting down client...')
        return True
    except:
        return False

def start_client(connection_ip: str) -> None:
    '''
    Starts the connection to the server, taking in an IP
    '''
    global _main_client, _valid_ports, _PORT, _HOST
    _HOST = connection_ip

    # overrides
    if len(_ov_ports) > 0:
        _valid_ports = _ov_ports
        _PORT = _valid_ports[0]
        pprint(f'[OVERRIDE] Overrided ports to: {_valid_ports}')
    
    # establish the connection to a port that the server is on
    _main_client, _PORT = _cycle_port(_main_client)