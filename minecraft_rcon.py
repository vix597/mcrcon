"""
Written by: Sean LaPlante
Figured out how it works from here:
    https://github.com/Tiiffi/mcrcon/blob/master/mcrcon.c
    --Thanks Tiiffi 
    and here
    http://wiki.vg/Rcon
    and here (mainly here)
    https://github.com/barneygale/MCRcon/blob/master/mcrcon.py
    --Thanks barneygale
"""
import argparse
import getpass
import sys
import os
from mcrcon import MCRcon

def main():
    parser = argparse.ArgumentParser(description="Send commands to a remote Minecraft console")
    parser.add_argument('-i','--ip',help="IP address of the server",required=True)
    parser.add_argument('-p','--port',help="Port for RCON on the server",required=True)
    parser.add_argument('-P','--password',help="Password for RCON on the server")

    args = parser.parse_args()

    if not args.password:
        pw = getpass.getpass()

    rcon = MCRcon(args.ip,int(args.port),pw)

    print("Type 'cls' or 'clear' to clear the screen")
    print("Type 'exit' or 'quit' or cntrl-c to exit")

    while 1:
        cmd = input('Remote Console>> ')
        if cmd == 'cls' or cmd == 'clear':
            os.system('cls')
        elif cmd == 'exit' or cmd == 'quit':
            rcon.close()
            sys.exit(0)
        elif cmd == "":
            pass
        else:
            print(rcon.send(cmd))

if __name__=="__main__":
    main()