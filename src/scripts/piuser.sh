#!/bin/bash
# recreate pi user
mkdir /home/pi
chown pi:pi /home/pi
useradd  -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,render,netdev,gpio,spi,i2c -d /home/pi pi
echo "pi:raspberry" | chpasswd
# remove root password
passwd -l root