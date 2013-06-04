import config
import os
import re
from tornado import tcpserver
from hashlib import sha1

_LOGOUT_CHECK = re.compile(r'[A-Z]{4}[0-9]{2} LOGOUT', re.U)


class ExpectTCPServer(tcpserver.TCPServer):
    """A simple TCP server that tries to match given, previouslly recorded
    incoming messages with the corresponding, previously seen response"""

    def handle_stream(self, stream, address):
        buf = {"data": ""}

        def _on_close(data):
            pass

        def _on_chunk(data):
            buf['data'] += data.encode(errors='replace')
            s = sha1()
            s.update(buf['data'])
            incoming_hash = s.hexdigest()
            possible_response_file = os.path.join(config.netdump_response_path, incoming_hash)
            if os.path.isfile(possible_response_file):
                handle = open(possible_response_file, 'r')
                response = handle.read()
                handle.close()
                buf['data'] = ""
                stream.write(response)
            elif _LOGOUT_CHECK.match(buf['data']):
                stream.close()

        stream.read_until_close(_on_close, streaming_callback=_on_chunk)


class ExpectIMAPServer(ExpectTCPServer):
    """A simple Expect style IMAP server that will send an "OK" messages
    the moment a connection is established, but then will act like a normal
    expect stream afterwards"""

    def handle_stream(self, stream, address):
        stream.write("* OK Gimap ready for requests from 131.193.34.208 s7if10537614oai.238\n")
        super(ExpectIMAPServer, self).handle_stream(stream, address)
