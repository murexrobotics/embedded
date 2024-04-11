# Security was not a concern when developing this program. Do not use in information sensitive enviornments.

import argparse
import subprocess
import os

username = "byran"
path_string = "/Users/byran/.local/bin:/Users/byran/.local/bin:/Users/byran/.opam/4.10.2/bin:/opt/homebrew/opt/llvm/bin:/Users/byran/.local/bin:/Applications/KiCad/KiCad.app/Contents/MacOS:/opt/homebrew/opt/qt@5/bin:/opt/homebrew/opt/llvm/bin:/opt/homebrew/opt/llvm/bin:/opt/homebrew/opt/qt@5/bin:/opt/local/bin:/opt/local/sbin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/opt/X11/bin:/Library/Apple/usr/bin:/Users/byran/.local/bin:/Users/byran/.opam/4.10.2/bin:/opt/homebrew/opt/llvm/bin:/Applications/KiCad/KiCad.app/Contents/MacOS:/opt/homebrew/opt/qt@5/bin:/opt/local/bin:/opt/local/sbin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/byran/.cargo/bin:/Users/byran/.orbstack/bin:/Users/byran/.spicetify:/Library/Frameworks/GStreamer.framework/Commands:/Users/byran/.orbstack/bin:/Users/byran/.spicetify:/Library/Frameworks/GStreamer.framework/Commands"
system_password = ""
ip_addr = "10.2.10.62"

prefix = "sshpass -p {} ssh {}@{}".format(system_password, username, ip_addr)

parser = argparse.ArgumentParser(description='MUREX Robotics diagnostics utility')
parser.add_argument('-ns', '--networkscan',
                    action='store_true')  # on/off flag
parser.add_argument('-i2c', '--i2cscan',
                    action='store_true')  # on/off flag
parser.add_argument('-ping', '--ping',
                    action='store_true')  # on/off flag

args = parser.parse_args()

print(args.ping, args.i2cscan)

if args.ping:
    os.system("{} 'ping 10.2.10.62' ".format(prefix))

if args.networkscan:
    os.system("{} 'sudo --stdin echo hello'".format(prefix))