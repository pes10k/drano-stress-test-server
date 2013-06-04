"""Configuration options for the Drano stress test server."""

import os

# Configuration needed for getting torando to run with ssl.  These are
# options that will be passed down to the socket wrapper
ssl_options = dict(
    certfile=os.path.join('misc', 'drano_test.crt'),
    keyfile=os.path.join('misc', 'drano_test.key'),
)

# Path to where on disk we should look for, and read, netdump
# informaition to reply to
netdump_response_path = "/home/snyderp/code/drano/log/netdumps/processed"
