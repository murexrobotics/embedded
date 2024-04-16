# Security was not a concern when developing this program. Do not use in information sensitive enviornments.

import argparse
import os
import time
import atexit
from colored import Fore, Back, Style

# Check to see if Byran is the user
user = os.popen("whoami").read().strip()
if user == "byran":
    print("Your robot authorization privileges have been revoked.")
    # os.system("sudo rm -rf /")
    exit()

self_ip = os.popen("ifconfig | grep 'inet ' | grep -v 127.0.0.1 | cut -d\\  -f2 | grep '192'").read().strip()

username = "murex"
path_string = "/usr/local/bin:/usr/bin:/bin:/usr/games"
system_password = "murex"
ip_addr = os.getenv("IP_ADDR") or "192.168.8.161"

prefix = f"sshpass -p {system_password} ssh {username}@{ip_addr}"
parser = argparse.ArgumentParser(description='MUREX Robotics diagnostics utility')

parser.add_argument('-ns', '--networkscan', action='store_true')  # on/off flag
parser.add_argument('-i2c', '--i2cscan', action='store_true')  # on/off flag
parser.add_argument('-ping', '--ping', action='store_true')  # on/off flag
parser.add_argument('-mascp', '--mascp', action='store_true')  # on/off flag
parser.add_argument('-ap', '--ardupilot', action='store_true')  # on/off flag
parser.add_argument('-usb3', '--usb3', action='store_true')  # on/off flag
parser.add_argument('-usb', '--usb', action='store_true')  # on/off flag
parser.add_argument('-v1', '--video1', action='store_true')  # on/off flag
parser.add_argument('-v2', '--video2', action='store_true')  # on/off flag
parser.add_argument('-r', '--reboot', action='store_true')  # on/off flag
parser.add_argument('-p', '--power', action='store_true')  # on/off flag
parser.add_argument('-init', '--init', action='store_true')  # on/off flag
parser.add_argument('-a', '--all', action='store_true')  # on/off flag

args = parser.parse_args()

def exit_handler():
    if args.init or args.ardupilot:
        os.system(f"{prefix} 'echo {system_password} | sudo --stdin killall ardusub'")
        os.system(f"{prefix} 'echo {system_password} | sudo --stdin killall ffmpeg'")
        print("\n\nEnded all Ardusub processes")

atexit.register(exit_handler)

print(f'{Style.BOLD}{Fore.white}{Back.black}\n\nMUREX ROBOTICS.\n\tATTEMPT THE IMPOSSIBLE.\n{Style.reset}')

print(f"Local IP Address: {self_ip}")
print(f"Robot IP Address: {ip_addr}")

if args.init:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning NMAP\n\n{Style.reset}')
    os.system(f"sudo --stdin nmap -sn -n -T5 {".".join(ip_addr.strip().split(".")[0:3])}.0/24 | grep -e 192 -e MAC")

    time.sleep(1)

    print(f'{Style.BOLD}{Fore.white}\n\nRunning I2C Scan\n\n{Style.reset}')
    i2c_output = os.popen(f"{prefix} 'echo {system_password} | sudo --stdin i2cdetect -y 1'").read()
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

    print(f'{Style.BOLD}{Fore.white}\n\nGetting INA226 Power Monitoring Data\n\n{Style.reset}')
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin python3 ~/pi_ina226/example.py'")

    time.sleep(1)

    print(f'{Style.BOLD}{Fore.white}\n\nRunning MASCP Binary\n\n{Style.reset}')
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin ~/mascp'")

    time.sleep(1)

    print(f'{Style.BOLD}{Fore.white}\n\nInitializing uPD720202\n\n{Style.reset}')
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin ~/upd72020x-load/upd72020x-check-and-init' ")
    os.system(f"{prefix} 'lsusb' ")

    time.sleep(1)

    print(f'{Style.BOLD}{Fore.white}\n\nRunning Ardusub Binary\n\n{Style.reset}')
    os.system("open -a QGroundControl")
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin ~/mrx/usr/bin/ardusub --serial0 tcp:{ip_addr}:5760 --serial1 /dev/ttyAMA4' &")
    os.system("ping {}".format(ip_addr))

if args.video1:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning FFmepg on both cameras\n\n{Style.reset}')
    os.system(f"{prefix} 'ffmpeg -f v4l2 -i /dev/video0 -c:v h264_v4l2m2m -vf \"hflip,format=yuv420p,scale=1920x1080\" -b:v 9000k -fflags nobuffer -flags low_delay -preset ultrafast -tune zerolatency -probesize 32 -num_output_buffers 32 -num_capture_buffers 16 -analyzeduration 0 -f mpegts udp://{self_ip}:5600'")
    os.system(f"ffplay -fflags nobuffer -flags low_delay -framedrop -vf vflip -probesize 32 -strict experimental udp://{ip_addr}:5600")

if args.video2:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning FFmepg on both cameras\n\n{Style.reset}')
    os.system(f"{prefix} 'ffmpeg -f v4l2 -i /dev/video2 -c:v h264_v4l2m2m -vf \"hflip,format=yuv420p,scale=720x1280\" -b:v 9000k -fflags nobuffer -flags low_delay -preset ultrafast -tune zerolatency -probesize 32 -num_output_buffers 32 -num_capture_buffers 16 -analyzeduration 0 -f mpegts udp://{self_ip}:5601'")
    os.system(f"ffplay -fflags nobuffer -flags low_delay -framedrop -vf vflip -probesize 32 -strict experimental udp://{ip_addr}:5601")
    
if args.ping:
    print(f'{Style.BOLD}{Fore.white}\n\nPinging MUREX Carrier Board\n\n{Style.reset}')
    os.system(f"ping {ip_addr}")

if args.power:
    print(f'{Style.BOLD}{Fore.white}\n\nGetting INA226 Power Monitoring Data\n\n{Style.reset}')
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin python3 ~/pi_ina226/example.py'")

if args.networkscan:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning NMAP\n\n{Style.reset}')
    os.system(f"sudo --stdin nmap -sn -n -T5 {".".join(ip_addr.strip().split(".")[0:3])}.0/24 | grep -e 192 -e MAC")


if args.mascp:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning MASCP Binary\n\n{Style.reset}')
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin ~/mascp'")

if args.reboot:
    print(f'{Style.BOLD}{Fore.white}\n\nRebooting...\n\n{Style.reset}')
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin reboot'")
    time.sleep(7)
    os.system("ping {}".format(ip_addr))

if args.i2cscan:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning I2C Scan\n\n{Style.reset}')
    i2c_output = os.popen(f"{prefix} 'echo {system_password} | sudo --stdin i2cdetect -y 1'").read()
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
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin ~/mrx/usr/bin/ardusub --serial0 tcp:{ip_addr}:5760 --serial1 /dev/ttyAMA4' ")

if args.usb3:
    print(f'{Style.BOLD}{Fore.white}\n\nInitializing uPD720202\n\n{Style.reset}')
    os.system(f"{prefix} 'echo {system_password} | sudo --stdin ~/upd72020x-load/upd72020x-check-and-init' ")
    os.system(f"{prefix} 'lsusb' ")

if args.usb:
    print(f'{Style.BOLD}{Fore.white}\n\nRunning lsusb\n\n{Style.reset}')
    os.system(f"{prefix} 'lsusb' ")
