"""Find Services Module"""
import socket


def find_services(min_port, max_port):
    """Returns a dict of services associated with a range of port values

    Args:
        min_port (int): Min port value. Must be greater than or equal to 0.
        max_port (int): Max port value. Must be less than or equal to 65535.

    Raises:
        ValueError: Min and Max port values out of range.

    Returns:
        dict: Dict of port/services
    """
    if min_port < 0 or max_port > 65535 or min_port > max_port:
        raise ValueError('Invalid min and max port values')

    services = {}
    for i in range(min_port, max_port + 1):
        try:
            service = socket.getservbyport(i)
        except OSError:
            print(f'Port {i} not associated with a service')
        else:
            services[i] = service

    return services
