![[Pasted image 20230503215152.png]]

`Linux mango 4.15.0-64-generic #73-Ubuntu SMP Thu Sep 12 13:16:13 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux`

```bash
╔══════════╣ Sudo version  
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#sudo-version  
Sudo version 1.8.21p2

╔══════════╣ Active Ports  
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#open-ports  
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp6       0      0 :::80                   :::*                    LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 :::443                  :::*                    LISTEN      -
```

## As user "admin"
```bash
╔══════════╣ Checking Pkexec policy    
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation/interesting-groups-linux-pe#pe-method-2

[Configuration]                                                             
AdminIdentities=unix-user:0

[Configuration]             
AdminIdentities=unix-group:sudo;unix-group:admin
```

## "Unknown SUID binary"
```
-rwsr-sr-- 1 root admin 11K Jul 18  2019 /usr/lib/jvm/java-11-openjdk-amd64/bin/jjs (Unknown SUID binary!)
```

![[Pasted image 20230503223328.png]]

![[Pasted image 20230503223541.png]]
```
Description

The `jjs` command-line tool is used to invoke the Nashorn engine. You can use it to interpret one or several script files, or to run an interactive shell.
```

![[Pasted image 20230503223921.png]]
However, this seems to completely lock-up the terminal and becomes unresponsive

![[Pasted image 20230503224745.png]]

Trying the file read method:
![[Pasted image 20230503224922.png]]

![[Pasted image 20230503225727.png]]

This could be used to modify system files and allow for manually escalating my privileges but that's a lot of work. I'd rather get a shell.

![[Pasted image 20230503230054.png]]

![[Pasted image 20230503230157.png]]