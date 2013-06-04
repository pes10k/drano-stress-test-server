"""Prepare training information by consuming a directory of recorded
plaintext network traffic and transforming it into a new directory
of responses, each named as the sha1 of the contents of the message
it is replying to"""


import os
from hashlib import sha1


def prepare(source_path, dest_path):
    """Takes all information dumped from network traffic and prepares them
    to be served back as responses.  The function prepares the network data
    by
        1. coallecing adjecent messages
        2. strip out HTTP headers (for HTTP(s) traffic)
        3. pairing the outgoing message with its response
        4. hash the outgoing message
        5. store the hash of the outgoing message with the body of the
           response / incoming message in mongo for future use

    Returns:
        The number of responses that were recorded, or None if there was
        some error (like the logging path not being configured)
    """
    if not os.path.isdir(source_path):
        raise Exception("Invalid path to netdump files: {path}".format(path=source_path))

    for root, dirs, files in os.walk(source_path):
        netdump_messages = [os.path.join(root, a_file) for a_file in files]

    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)
    netdump_messages.sort()
    last_was_incoming = True
    outgoing_hash = False
    buf = ""
    count = 0

    for log in netdump_messages:
        is_incoming = "response" in log

        # If the traffic we're reading is continuing in the same direction
        # (ex we're reading an outgoing response after reading an outgoing
        # response)
        if last_was_incoming == is_incoming:
            buf += open(log, 'r').read()
        elif is_incoming:
            # Else, if we were looking at outgoing messages, but now see
            # a response starting, we should hash the current buffer and
            # start building a new one
            s = sha1()
            s.update(buf.encode(errors='replace'))
            outgoing_hash = s.hexdigest()
            log_handle = open(log, 'r')
            buf = log_handle.read()
            log_handle.close()
        elif outgoing_hash:
            # Otherwise, if we're switching back to reading a new outgoing
            # message, then it means we've now completed everything we need
            # to store a outgoing / incoming pair.  We should now store
            # this pair in mongo and continue on
            dest_file = os.path.join(dest_path, outgoing_hash)
            if not os.path.isfile(dest_file):
                handle = open(dest_file, 'w')
                handle.write(buf)
                handle.close()
                count += 1
            log_handle = open(log, 'r')
            buf = log_handle.read()
            log_handle.close()
        last_was_incoming = is_incoming
    return count

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process netdump data into response files.')
    parser.add_argument('-s', type=str, required=True,
                        help='path to a directory of netdump data')
    parser.add_argument('-d', type=str, required=True,
                        help='path to directory to write response files')

    args = parser.parse_args()
    print prepare(args.s, args.d)
