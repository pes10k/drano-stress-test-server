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

# Connection parameters for connecting to persistant store
mongo = dict(
    dbname='',
    pool_id='',
    port=27017,
    host="127.0.0.1"
)
