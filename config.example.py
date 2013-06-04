"""Configuration options for the Drano stress test server."""

import ssl

# Configuration needed for getting torando to run with ssl.  These are
# options that will be passed down to the socket wrapper
ssl_options = dict(
    certfile=None,
    keyfile=None,
    ciphers="ALL",
    ssl_version=ssl.PROTOCOL_SSLv3,
)

# Path to where on disk we should look for, and read, netdump
# informaition to reply to
netdump_response_path = ""
