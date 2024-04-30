**These are the linux driver files for the Lake Shore Cryotronics 240 Series Model 240-8P**

**Installation guide:**

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
depmod # re-read module dependencies
```

Then load in the files:
```bash
insmod /usr/lib/modules/`uname -r`/kernel/drivers/usb/serial/usbserial.ko 
insmod /root/Silabs/5.13/Linux_3.x.x_4.x.x_VCP_Driver_Source/cp210x.ko
```
**Extra information about the drivers:**
-  The original drivers were downloaded from https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads
-  The drivers were edited for the lakeshore model 240-8P:

Tweaked c as per: https://community.silabs.com/s/question/0D58Y00008u8b0SSAQ/cp210x-to-vcp-driver-failed-to-build-for-kernel-513-ubuntu-2004?language=en_US
```bash
root@regor:~/Silabs# diff -u cp210x.c 5.13/Linux_3.x.x_4.x.x_VCP_Driver_Source/cp210x.c 
--- cp210x.c	2024-02-12 15:11:23.660179231 +0100
+++ 5.13/Linux_3.x.x_4.x.x_VCP_Driver_Source/cp210x.c	2024-02-12 15:18:40.294921769 +0100
@@ -49,7 +49,7 @@
 static void cp210x_disconnect(struct usb_serial *);
 static void cp210x_release(struct usb_serial *);
 static int cp210x_port_probe(struct usb_serial_port *);
-static int cp210x_port_remove(struct usb_serial_port *);
+static void cp210x_port_remove(struct usb_serial_port *);
 static void cp210x_dtr_rts(struct usb_serial_port *p, int on);
 static int cp210x_suspend(struct usb_serial *, pm_message_t);
 static int cp210x_resume(struct usb_serial *);
@@ -2412,14 +2412,12 @@
 	return 0;
 }
 
-static int cp210x_port_remove(struct usb_serial_port *port)
+static void cp210x_port_remove(struct usb_serial_port *port)
 {
 	struct cp210x_port_private *port_priv;
 
 	port_priv = usb_get_serial_port_data(port);
 	kfree(port_priv);
-
-	return 0;
 }
 
 static void cp210x_init_max_speed(struct usb_serial *serial)
```

Tweaked Makefile:
```bash
root@regor:~/Silabs# diff Makefile Makefile.old 
2c2
< KDIR = /sys/kernel/btf/vmlinux
---
> KDIR = /lib/modules/`uname -r`/build
```

Load:
```bash
insmod /usr/lib/modules/`uname -r`/kernel/drivers/usb/serial/usbserial.ko 
insmod /root/Silabs/5.13/Linux_3.x.x_4.x.x_VCP_Driver_Source/cp210x.ko
```
