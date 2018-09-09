"""Echo Server"""
import socket
import sys
import logging
import queue
from select import select

BUFF_SIZE = 16


def server(log_buffer=sys.stderr):
    logging.basicConfig(level=logging.INFO, stream=log_buffer)
    logger = logging.getLogger(__name__)

    # set an address for our server
    address = ('127.0.0.1', 10000)

    server = socket.socket(family=socket.AF_INET,
                           type=socket.SOCK_STREAM,
                           proto=socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)

    # log that we are building a server
    logger.info(f'making a server on {address[0]}:{address[1]}')

    server.bind(address)
    server.listen(5)

    inputs = [server]
    outputs = []
    message_queues = {}
    connections = 0

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while inputs:
            readable, writable, exceptional = select(inputs, outputs, inputs)

            for s in readable:
                if s is server:
                    conn, addr = server.accept()
                    connections += 1

                    logger.info(f'connection - {addr[0]}:{addr[1]}')
                    logger.info(f'{connections} active connections')
                    conn.setblocking(False)
                    inputs.append(conn)
                    message_queues[conn] = queue.Queue()
                else:
                    data = s.recv(BUFF_SIZE)
                    logger.info(f'received "{data.decode("utf-8")}"')

                    if data:
                        message_queues[s].put(data)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]
                        connections -= 1
                        logger.info('echo complete, client connection closed')
                        logger.info(f'{connections} active connections')

            for s in writable:
                try:
                    data = message_queues[s].get_nowait()
                except queue.Empty:
                    outputs.remove(s)
                else:
                    s.sendall(data)
                    logger.info(f'sent "{data.decode("utf-8")}"')

            for s in exceptional:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]
                connections -= 1
                logger.info('Error with client, connection closed')
                logger.info(f'{connections} active connections')
    except KeyboardInterrupt:
        for s in inputs:
            s.close()
        message_queues.clear()
        logger.info('quitting echo server')


if __name__ == '__main__':
    server()
    sys.exit(0)
