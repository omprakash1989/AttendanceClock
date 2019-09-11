import socket
import logging

import socks

from settings import ProxyServerEnum

logger = logging.getLogger('punching_clock')


class SocketClient:
    """Socket client to be used for CIBIL integration"""

    def __init__(self, sock=None, timeout=None, through_proxy=None):
        through_proxy = bool(through_proxy) if through_proxy else ProxyServerEnum.ACTIVE.value
        if sock is None:
            self.sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            if through_proxy:
                if ProxyServerEnum.HOST.value and ProxyServerEnum.PORT.value:
                    self.sock.set_proxy(
                        proxy_type=socks.SOCKS5,
                        addr=ProxyServerEnum.HOST.value,
                        port=ProxyServerEnum.PORT.value,
                    )
                else:
                    logger.warning("No proxy host and (or) port not found. Proceeding without proxy.")
        else:
            self.sock = sock

        # Set timeout.
        self.sock.settimeout(timeout)

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
        except socket.timeout:
            logger.exception("Connection to AttendanceClock Service timed out")
        except OSError:
            logger.exception(
                "Failed to connect to {d} via proxy {p}".format(
                    d=str(host) + ":" + str(port),
                    p=str(ProxyServerEnum.HOST.value) + ":" + str(ProxyServerEnum.PORT.value),
                ))

    def send(self, msg, termination_char):
        total_sent = 0
        try:
            while total_sent < len(msg):
                sent = self.sock.send(msg[total_sent:])
                if sent == 0:
                    raise RuntimeError
                total_sent = total_sent + sent
            self.sock.send(termination_char)

        except socket.timeout:
            logger.exception("Connection to AttendanceClock Service timed out")

        except RuntimeError:
            logger.exception("Connection broken to punching_clock service.")

        return total_sent

    def receive(self, termination_char):
        chunks = []
        bytes_recd = 0
        last_char = b'T'
        try:
            while last_char != termination_char:
                chunk = self.sock.recv(256)
                if chunk == b'':
                    raise RuntimeError
                chunks.append(chunk.decode('utf-8'))
                last_char = chunk[len(chunk)-1:]
                bytes_recd += len(chunk)

        except socket.timeout:
            logger.exception("Connection to AttendanceClock Service timed out after receiving chucks: {}".format(chunks))
            chunks = []

        except RuntimeError:
            logger.exception("Connection broken to punching_clock service after receiving chucks: {}.".format(chunks))

        finally:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()

        return ''.join(chunks)
