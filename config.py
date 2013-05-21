"""Configuration options for the Drano stress test server."""

import os

# Configuration needed for getting torando to run with ssl.  These are
# options that will be passed down to the socket wrapper
ssl_options = dict(
    certfile=os.path.join('misc', 'drano_test.crt'),
    keyfile=os.path.join('misc', 'drano_test.key'),
)

# Connection parameters for connecting to persistant store
mongo = dict(
    dbname='drano',
    pool_id='webapp',
    port=27017,
    host="127.0.0.1"
)
