I do not have pepper's password.

Very serious IOC:
![[Pasted image 20230504210521.png]]

whatever tho...

## Root files in home dir
```
╔══════════╣ Searching root files in home dirs (limit 30)  
/home/  
/home/pepper/user.txt  
/home/pepper/.bash_history  
/home/pepper/Web/Logs/10.10.16.2.txt

╔══════════╣ Readable files belonging to root and readable by me but not world readable  
-rwsr-x--- 1 root pepper 174520 Feb 17  2019 /bin/systemctl  
-r--r----- 1 root pepper 33 May  3 23:06 /home/pepper/user.txt
```


## /bin/systemctl
![[Pasted image 20230504211250.png]]
![[Pasted image 20230504211937.png]]

I have access to systemctl...

I can create a service unit on the system for `systemctl` to run, potentially giving me a root shell.

https://medium.com/@klockw3rk/privilege-escalation-leveraging-misconfigured-systemctl-permissions-bc62b0b28d49

![[Pasted image 20230504212633.png]]
![[Pasted image 20230504212525.png]]
