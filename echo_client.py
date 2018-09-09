"""Echo Clinet"""
import socket
import sys
import traceback
import logging

BUFF_SIZE = 16


def client(msg, log_buffer=sys.stderr):
    """Client function in client-server echo program

    Args:
        msg (string): Message to be echoed by server
        log_buffer (stream, optional): Defaults to sys.stderr.

    Returns:
        string: Echoed string
    """
    logging.basicConfig(level=logging.INFO, stream=log_buffer)
    logger = logging.getLogger(__name__)

    server_address = ('localhost', 10000)
    sock = socket.socket(family=socket.AF_INET,
                         type=socket.SOCK_STREAM,
                         proto=socket.IPPROTO_TCP)

    logger.info('connecting to {server_address[0]} port {server_address[1]}')
    sock.connect(server_address)

    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        logger.info('sending "{msg}"')
        sock.sendall(msg.encode('utf-8'))

        while True:
            chunk = sock.recv(BUFF_SIZE)
            if not chunk:
                break

            received_message = ''.join([received_message, chunk.decode('utf-8')])
            logger.info(f'received "{chunk.decode("utf-8")}"')
    except Exception:
        traceback.print_exc()
        sys.exit(1)
    finally:
        sock.close()
        logger.info('closing socket')

    return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    message = sys.argv[1]
    print(client(message))
