import socket
import struct
import select

#-------RCON Packet------
    #int Length
    #int request ID (client-generated)
    #int type (2 = run command, 3 = login)
    #byte[] payload (ASCII text)
    #2 NULL bytes at the end as padding
#------------------------

class MCRcon(object):
    #Type values (these values are not made up)
    RUN_COMMAND = 2
    AUTH = 3

    #Request ID value (I made this up, use whatever you want, except -1)
    #Server returns same value on success -1 on failure
    RCON_REQ_ID = 7

    #Size of 2 int values and 2 NULL bytes. Remember to add len(cmd)
    PACKET_SIZE = 10

    def __init__(self,ip,port,password):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.password = password
        self.sock.connect((self.ip,self.port))
        self.authenticate()

    def authenticate(self):
        self.send_real(self.password,self.AUTH)

    def send(self,cmd):
        return self.send_real(cmd,self.RUN_COMMAND)

    def send_real(self,cmd,cmd_type):
        packet = None
        packet = struct.pack(
            '<iii',
            self.PACKET_SIZE + len(cmd),
            self.RCON_REQ_ID,
            cmd_type
        ) + str.encode(cmd) + b'\x00\x00'

        self.sock.send(packet)

        more_data = True
        ret_data = b""
        while more_data:
            length, req_id, cmd_type = struct.unpack('<iii',self.sock.recv(12))
            data = self.sock.recv(length-8)

            if req_id != self.RCON_REQ_ID:
                raise Exception('Protocol failure', 'wrong returned request ID')
            elif data[-2:] != b'\x00\x00':
                raise Exception('Protocol failure', 'non-null pad bytes')

            print("DEBUG: data is\n============================\n",data,"\n==============================\n")
            ret_data += data[:-2]

            more_data = select.select([self.sock], [], [],0)[0]
        return ret_data.decode('utf-8')

    def close(self):
        self.sock.close()