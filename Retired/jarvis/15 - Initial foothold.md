```
                               ╔═══════════════════╗
═══════════════════════════════╣ Basic information 

OS: Linux version 4.9.0-8-amd64 (debian-kernel@lists.debian.org) (gcc version 6.3.0 20170516 (Debian 6.3.0-18+deb9u1) ) #1 SMP Debian 4.9.144-3.1 (2019-02-19)

User & Groups: uid=33(www-data) gid=33(www-data) groups=33(www-data)
Hostname: jarvis
Writable folder: /dev/shm

[+] /bin/ping is available for network discovery (linpeas can discover hosts, learn more with -h)

[+] /bin/bash is available for network discovery, port scanning and port forwarding (linpeas can discover hosts, scan ports, and forward ports. Learn more with -h)

[+] /bin/nc is available for network discovery & port scanning (linpeas can discover hosts and scan ports, learn more with -h)
```

```
                      ╔════════════════════════════════════╗
══════════════════════╣ Files with Interesting Permissions 

╔══════════╣ SUID - Check easy privesc, exploits and write perms
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-and-suid
strace Not Found

-rwsr-xr-x 1 root root 44K Mar  7  2018 /bin/mount  --->  Apple_Mac_OSX(Lion)_Kernel_xnu-1699.32.7_except_xnu-1699.24.8

-rwsr-x--- 1 root pepper 171K Feb 17  2019 /bin/systemctl (Unknown SUID binary!)
-rwsr-xr-x 1 root root 31K Mar  7  2018 /bin/umount  --->  BSD/Linux(08-1996)
-rwsr-xr-x 1 root root 40K May 17  2017 /usr/bin/newgrp  --->  HP-UX_10.20
-rwsr-xr-x 1 root root 59K May 17  2017 /usr/bin/passwd  --->  Apple_Mac_OSX(03-2006)/Solaris_8/9(12-2004)/SPARC_8/9/Sun_Solaris_2.3_to_2.5.1(02-1997)
-rwsr-xr-x 1 root root 138K Jun  5  2017 /usr/bin/sudo  --->  check_if_the_sudo_version_is_vulnerable
-rwsr-xr-x 1 root root 49K May 17  2017 /usr/bin/chfn  --->  SuSE_9.3/10
```

`/bin/systemctl` does not seem to be a normal binary according to linpeas. Normally, `systemctl` is located in `/usr/bin/systemctl`.

## sudo
![[Pasted image 20230504035938.png]]
![[Pasted image 20230504040110.png]]

Possible arbitrary code execution. However, i'm not allowed to add special characters or logical operators:
```python
def exec_ping():
    forbidden = ['&', ';', '-', '`', '||', '|']
    command = input('Enter an IP: ')
    for i in forbidden:
        if i in command:
            print('Got you')
            exit()
    os.system('ping ' + command)
```

Invocation:
```python
if __name__ == '__main__':
	show_header()
...
	elif sys.argv[1] == '-p':
	    exec_ping()
	    exit()
```

What they didn't realize is that bash commands can be concatenated in with `$()`. This means I can run a bash script in `$(/tmp/reverse_shell.sh).`

![[Pasted image 20230504043035.png]]

