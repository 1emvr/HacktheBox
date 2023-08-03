![[Pasted image 20230503171518.png]]

It looks like the sed command is not available on this system, so using linpeas will not work. There might be a chance that linenum could work.

- Sunny is part of the `staff` group.

## System info
`SunOS sunday 5.11 11.4.0.15.0 i86pc i386 i86pc`

```
[-] Specific release information:  

NAME="Oracle Solaris"  
PRETTY_NAME="Oracle Solaris 11.4"  
CPE_NAME="cpe:/o:oracle:solaris:11:4"  
ID=solaris  
VERSION=11.4  
VERSION_ID=11.4  
BUILD_ID=11.4.0.0.1.15.0  
HOME_URL="https://www.oracle.com/solaris/"  
SUPPORT_URL="https://support.oracle.com/"

[+] We can sudo without supplying a password!

User sunny may run the following commands on sunday:  
   (root) NOPASSWD: /root/troll

[-] Root is allowed to login via SSH:  
PermitRootLogin yes


```

## /backup
![[Pasted image 20230503173436.png]]

![[Pasted image 20230503173507.png]]

![[Pasted image 20230503173658.png]]

![[Pasted image 20230503173942.png]]
`sammy:cooldude!`

## /root/troll
```bash
sunny@sunday:/tmp$ sudo /root/troll  
testing  
uid=0(root) gid=0(root)
```

it just runs `id`. The name `troll` is fitting.

