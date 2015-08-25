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
import platform
from mcrcon import MCRcon

def main():
    if platform.system() == "Windows":
        clear_str = 'cls'
    else:
        clear_str = 'clear'

    parser = argparse.ArgumentParser(description="Send commands to a remote Minecraft console")
    parser.add_argument('-h','--ip',help="IP address of the server",required=True)
    parser.add_argument('-p','--port',help="Port for RCON on the server",required=True)

    args = parser.parse_args()

    if not args.password:
        pw = getpass.getpass()

    rcon = MCRcon(args.ip,int(args.port),pw)

    print("Type 'cls' or 'clear' to clear the screen")
    print("Type 'exit' or 'quit' or cntrl-c to exit")

    while 1:
        try:
            cmd = str(input('Remote Console>> '))
            if cmd.strip().lower() in ['cls', 'clear']:
                os.system(clear_str)
            elif cmd.strip().lower() in ['exit', 'quit']:
                rcon.close()
                exit(0)
            elif cmd.strip() == "":
                pass
            else:
                print(rcon.send(cmd))
        except EOFError:
            print("ctrl-d detected, exiting...")
            exit(0)

if __name__=="__main__":
    main()