"""Echo Server"""
import socket
import sys
import traceback
import logging

BUFF_SIZE = 16


def server(log_buffer=sys.stderr):
    logging.basicConfig(level=logging.INFO, stream=log_buffer)
    logger = logging.getLogger(__name__)

    # set an address for our server
    address = ('127.0.0.1', 10000)

    sock = socket.socket(family=socket.AF_INET,
                         type=socket.SOCK_STREAM,
                         proto=socket.IPPROTO_TCP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    logger.info(f'making a server on {address[0]}:{address[1]}')

    sock.bind(address)
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            logger.info('waiting for a connection')

            conn, addr = sock.accept()
            try:
                logger.info(f'connection - {addr[0]}:{addr[1]}')

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    data = conn.recv(BUFF_SIZE)
                    logger.info(f'received "{data.decode("utf-8")}"')

                    conn.sendall(data)
                    logger.info(f'sent "{data.decode("utf-8")}"')

                    if len(data) < BUFF_SIZE:
                        break
            except Exception:
                traceback.print_exc()
                sys.exit(1)
            finally:
                conn.close()
                logger.info('echo complete, client connection closed')

    except KeyboardInterrupt:
        sock.close()
        logger.info('quitting echo server')


if __name__ == '__main__':
    server()
    sys.exit(0)
