# -*- coding: utf-8 -*-
#*****************************************************************************
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#*****************************************************************************
from __future__ import print_function, unicode_literals, absolute_import

import socket, logging, logging.handlers
from _pline.unicode_helper import ensure_str

host = "localhost"
port = logging.handlers.DEFAULT_TCP_LOGGING_PORT


_pline_logger = logging.getLogger('_pline')
_pline_logger.setLevel(logging.DEBUG)
_pline_logger.propagate = False
formatter = logging.Formatter(str('%(message)s'))
file_handler = None

class NULLHandler(logging.Handler):
    def emit(self, s):
        pass

class SocketStream(object):
    def __init__(self, host, port):
        self.logsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def write(self, s):
        self.logsocket.sendto(ensure_str(s), (host, port))

    def flush(self):
        pass

    def close(self):
        pass

socket_handler = None
_pline_logger.addHandler(NULLHandler())

def start_socket_log():
    global socket_handler
    socket_handler = logging.StreamHandler(SocketStream(host, port))
    socket_handler.setFormatter(formatter)
    _pline_logger.addHandler(socket_handler)

def stop_socket_log():
    global socket_handler
    if socket_handler:
        _pline_logger.removeHandler(socket_handler)
        socket_handler = None

def start_file_log(filename):
    global file_handler
    file_handler = logging.FileHandler(filename, "w")
    _pline_logger.addHandler(file_handler)

def stop_file_log():
    global file_handler
    if file_handler:
        _pline_logger.removeHandler(file_handler)
        file_handler.close()
        file_handler = None

def stop_logging():
    log("STOPING LOG")
    stop_file_log()
    stop_socket_log()

def log(s):
    s = ensure_str(s)
    _pline_logger.debug(s)
