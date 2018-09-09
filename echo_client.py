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
    socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP),
             socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)]

    logger.info(f'connecting to {server_address[0]} port {server_address[1]}')
    for s in socks:
        s.connect(server_address)

    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        for s in socks:
            logger.info(f'sending "{msg}"')
            s.sendall(msg.encode('utf-8'))

        for s in socks:
            while True:
                chunk = s.recv(BUFF_SIZE)
                received_message += chunk.decode('utf-8')
                logger.info(f'received "{chunk.decode("utf-8")}"')

                if len(chunk) < BUFF_SIZE:
                    break
    except Exception:
        traceback.print_exc()
        sys.exit(1)
    finally:
        for s in socks:
            s.close()
        logger.info(f'closing sockets')

    return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    message = sys.argv[1]
    print(client(message))
