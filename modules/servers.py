import config
import tornado.netutil
from pymongo import MongoClient
from hashlib import sha1


client = MongoClient(config.mongo['host'], config.mongo['port'])
collection = client[config.mongo['dbname']].netdump_responses


class ExpectTCPServer(tornado.netutil.TCPServer):
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
            doc = collection.find_one({"_id": incoming_hash})
            if doc:
                response = doc['response'].encode('utf-8')
                buf['data'] = ""
                stream.write(response)
            elif "OIIJ15 LOGOUT" in buf['data']:
                stream.close()

        stream.read_until_close(_on_close, streaming_callback=_on_chunk)


class ExpectIMAPServer(ExpectTCPServer):
    """A simple Expect style IMAP server that will send an "OK" messages
    the moment a connection is established, but then will act like a normal
    expect stream afterwards"""

    def handle_stream(self, stream, address):
        stream.write("* OK Gimap ready for requests from 131.193.34.208 s7if10537614oai.238\n")
        super(ExpectIMAPServer, self).handle_stream(stream, address)
