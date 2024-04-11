# Security was not a concern when developing this program. Do not use in information sensitive enviornments.

import argparse
import os
import time
import atexit
from colored import Fore, Back, Style

def exit_handler():
    if args.init or args.ardupilot:
        os.system("{} 'echo {} | sudo --stdin killall ardusub'".format(prefix, system_password))
        print("\n\nEnded all Ardusub processes")

atexit.register(exit_handler)

self_ip = os.popen("ifconfig | grep 'inet ' | grep -v 127.0.0.1 | cut -d\\  -f2 | grep '192'").read()

username = "murex"
path_string = "/usr/local/bin:/usr/bin:/bin:/usr/games"
system_password = "murex"
ip_addr = "192.168.8.161"

prefix = "sshpass -p {} ssh {}@{}".format(system_password, username, ip_addr)

parser = argparse.ArgumentParser(description='MUREX Robotics diagnostics utility')
parser.add_argument('-ns', '--networkscan',
                    action='store_true')  # on/off flag
parser.add_argument('-i2c', '--i2cscan',
                    action='store_true')  # on/off flag
parser.add_argument('-ping', '--ping',
                    action='store_true')  # on/off flag
parser.add_argument('-mascp', '--mascp',
                    action='store_true')  # on/off flag
parser.add_argument('-ap', '--ardupilot',
                    action='store_true')  # on/off flag
parser.add_argument('-usb3', '--usb3',
                    action='store_true')  # on/off flag
parser.add_argument('-usb', '--usb',
                    action='store_true')  # on/off flag
parser.add_argument('-ffmpeg', '--ffmpeg',
                    action='store_true')  # on/off flag
parser.add_argument('-r', '--reboot',
                    action='store_true')  # on/off flag
parser.add_argument('-init', '--init',
                    action='store_true')  # on/off flag

args = parser.parse_args()

print(f'{Style.BOLD}{Fore.white}{Back.black}\n\nMUREX ROBOTICS.\n\tATTEMPT THE IMPOSSIBLE.\n{Style.reset}')

print("Local IP Address: {}".format(self_ip))

if args.init:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning NMAP\n\n{Style.reset}')
    os.system("sudo --stdin nmap -sn -n -T5 192.168.8.0/24 | grep -e 192 -e MAC")

    time.sleep(1)

    print(f'{Style.BOLD}{Fore.white}\n\nRunning I2C Scan\n\n{Style.reset}')
    i2c_output = os.popen("{} 'echo {} | sudo --stdin i2cdetect -y 1'".format(prefix, system_password)).read()
    print(i2c_output)
    if "77" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}BME680 at 0x77 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}BME680 at 0x77 NOT found!\n{Style.reset}')
    if "18" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}BMI088 Accel at 0x18 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}BMI088 Accel at 0x18 NOT found!\n{Style.reset}')
    if "68" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}BMI088 Gyro at 0x68 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}BMI088 Gyro at 0x68 NOT found!\n{Style.reset}')
    if "1c" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}LIS3MDL at 0x1C found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}LIS3MDL at 0x1C NOT found!\n{Style.reset}')
    if "76" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}MS5837 at 0x76 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}MS5837 at 0x76 NOT found!\n{Style.reset}')
    if "45" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}INA226 at 0x45 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}INA226 at 0x45 NOT found!\n{Style.reset}')

    time.sleep(1)

    print(f'{Style.BOLD}{Fore.white}\n\nRunning MASCP Binary\n\n{Style.reset}')
    os.system("{} 'echo {} | sudo --stdin ~/mascp'".format(prefix, system_password))

    time.sleep(1)

    print(f'{Style.BOLD}{Fore.white}\n\nInitializing uPD720202\n\n{Style.reset}')
    os.system("{} 'echo {} | sudo --stdin ~/upd72020x-load/upd72020x-check-and-init' ".format(prefix, system_password))
    os.system("{} 'lsusb' ".format(prefix))

    time.sleep(1)

    print(f'{Style.BOLD}{Fore.white}\n\nRunning Ardusub Binary\n\n{Style.reset}')
    os.system("open -a QGroundControl")
    os.system("{} 'echo {} | sudo --stdin ~/mrx/usr/bin/ardusub --serial0 tcp:192.168.8.161:5760 --serial1 /dev/ttyAMA4' ".format(prefix, system_password))

if args.ffmpeg:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning FFmepg on both cameras\n\n{Style.reset}')
    os.system("ffplay -fflags nobuffer -flags low_delay -framedrop -vf vflip -probesize 32 -strict experimental udp://{}:5601".format(ip_addr))
    os.system("{} 'echo {} | sudo --stdin echo altan_sucks' ".format(prefix, system_password))
    os.system("ffplay -fflags nobuffer -flags low_delay -framedrop -vf vflip -probesize 32 -strict experimental udp://{}:5602".format(ip_addr))
    os.system("{} 'echo {} | sudo --stdin echo altan_sucks' ".format(prefix, system_password))

if args.ping:
    print(f'{Style.BOLD}{Fore.white}\n\nPinging MUREX Carrier Board\n\n{Style.reset}')
    os.system("ping {}".format(ip_addr))

if args.networkscan:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning NMAP\n\n{Style.reset}')
    os.system("sudo --stdin nmap -sn -n -T5 192.168.8.0/24 | grep -e 192 -e MAC")

if args.mascp:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning MASCP Binary\n\n{Style.reset}')
    os.system("{} 'echo {} | sudo --stdin ~/mascp'".format(prefix, system_password))

if args.reboot:
    print(f'{Style.BOLD}{Fore.white}\n\nRebooting...\n\n{Style.reset}')
    os.system("{} 'echo {} | sudo --stdin reboot'".format(prefix, system_password))
    time.sleep(7)
    os.system("ping {}".format(ip_addr))

if args.i2cscan:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning I2C Scan\n\n{Style.reset}')
    i2c_output = os.popen("{} 'echo {} | sudo --stdin i2cdetect -y 1'".format(prefix, system_password)).read()
    if "77" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}BME680 at 0x77 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}BME680 at 0x77 NOT found!\n{Style.reset}')
    if "18" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}BMI088 Accel at 0x18 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}BMI088 Accel at 0x18 NOT found!\n{Style.reset}')
    if "68" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}BMI088 Gyro at 0x68 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}BMI088 Gyro at 0x68 NOT found!\n{Style.reset}')
    if "1c" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}LIS3MDL at 0x1C found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}LIS3MDL at 0x1C NOT found!\n{Style.reset}')
    if "76" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}MS5837 at 0x76 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}MS5837 at 0x76 NOT found!\n{Style.reset}')
    if "45" in i2c_output:
        print(f'{Style.BOLD}{Fore.green}INA226 at 0x45 found!\n{Style.reset}')
    else:
        print(f'{Style.BOLD}{Fore.red}INA226 at 0x45 NOT found!\n{Style.reset}')

if args.ardupilot:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning Ardusub Binary\n\n{Style.reset}')
    os.system("open -a QGroundControl")
    os.system("{} 'echo {} | sudo --stdin ~/mrx/usr/bin/ardusub --serial0 tcp:192.168.8.161:5760 --serial1 /dev/ttyAMA4' ".format(prefix, system_password))

if args.usb3:
    print(f'{Style.BOLD}{Fore.white}\n\nInitializing uPD720202\n\n{Style.reset}')
    os.system("{} 'echo {} | sudo --stdin ~/upd72020x-load/upd72020x-check-and-init' ".format(prefix, system_password))
    os.system("{} 'lsusb' ".format(prefix))

if args.usb:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning lsusb\n\n{Style.reset}')
    os.system("{} 'lsusb' ".format(prefix))
