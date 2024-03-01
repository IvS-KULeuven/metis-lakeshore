These are the linux driver files for the Lake Shore Cryotronics 240 Series Model 240-8P

Installation guide:

Place the /Silabs directory into your /root folder
```bash
cp -r Silabs /root
``` 
You have to do these commands anytime your kernel version changes, you can check your kernel version with
```bash
uname -a
```
These are the commands:
```bash
cd /root/Silabs/5.13/Linux_3.x.x_4.x.x_VCP_Driver_Source
make clean
make
cp /root/Silabs/5.13/Linux_3.x.x_4.x.x_VCP_Driver_Source/cp210x.ko /usr/lib/modules/`uname -r`/kernel/drivers/usb/serial/cp210x.ko
depmod # lees module dependencies opnieuw in
```

Then load in the files:
```bash
insmod /usr/lib/modules/`uname -r`/kernel/drivers/usb/serial/usbserial.ko 
insmod /root/Silabs/5.13/Linux_3.x.x_4.x.x_VCP_Driver_Source/cp210x.ko
```
