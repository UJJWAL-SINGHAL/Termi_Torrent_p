import random
import struct

class udpConnectionHelper:
    '''
        This is used with a UDP Tracker, upon
        very first connection. This is kind of
        like a handshake.

        64 + 32 + 32 bits = 128 bits = 16 bytes
    '''
   
    # The thing that I kept messing up was the endian order
    # If you don't put >, it struct.pack assumes native size or something
    # https://docs.python.org/2/library/struct.html

    def pack_payload(self):
        self.transaction_id = random.randint(1, 2 ** 31)
        return 0x41727101980.to_bytes(8, byteorder='big') + 0x0.to_bytes(4, byteorder='big') + self.transaction_id.to_bytes(4, byteorder='big')
    
    # We get 16 bytes back, 4 bytes = action, 4 bytes = trans_id, 8 bytes = connection_id
    # Returns connection id
    def unpack_payload(self, payload):
        hex_string = payload.hex() # grab the hex value of the payload
        
        action = int(hex_string[ : 8], 16)
        trans_id = int(hex_string[8 : 16], 16)
        conn_id = int(hex_string[16 : ], 16)

        # 
        assert trans_id == self.transaction_id, 'Received invalid transaction id'
        assert action == 0, 'Received action that was not 0, must have error\'d out'

        return conn_id
