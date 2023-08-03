![[Pasted image 20230408032819.png]]
Something strange about this Debian box. There isn't a lot of standard tools available. There isn't even sudo available and I can't change directories. Clearly this has been sandboxed.

![[Pasted image 20230408033146.png]]
I'm only able to read certain files. Again, `cd` is restricted

![[Pasted image 20230408033324.png]]
![[Pasted image 20230408033609.png]]

These appear to be some available commands. `Env` might be the most interesting one. It also seems like James and Mindy are the only 2 users on this box.
```
james:x:1000:1000:james:/home/james/:/bin/bash  
mindy:x:1001:1001:mindy:/home/mindy:/bin/rbash
```

James seems to have a full spread in his home directory, unlike Mindy:
```
mindy@solidstate:~$ ls -alh /home/james  
total 80K  
drwxr-xr-x 16 james osboxes 4.0K Apr 26  2021 .  
drwxr-xr-x  4 root  root    4.0K Apr 26  2021 ..  
lrwxrwxrwx  1 root  root       9 Apr 26  2021 .bash_history -> /dev/null  
-rw-r--r--  1 james osboxes  220 Jun 18  2017 .bash_logout  
-rw-r--r--  1 james osboxes 3.5K Jun 18  2017 .bashrc  
drwx------  8 james osboxes 4.0K Apr 26  2021 .cache  
drwx------ 10 james osboxes 4.0K Apr 26  2021 .config  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 Desktop  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 Documents  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 Downloads  
drwx------  3 james osboxes 4.0K Apr 26  2021 .gnupg  
-rw-------  1 james osboxes  640 Aug 22  2017 .ICEauthority  
drwxr-xr-x  3 james osboxes 4.0K Apr 26  2021 .local  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 Music  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 .nano  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 Pictures  
-rw-r--r--  1 james osboxes  675 Jun 18  2017 .profile  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 Public  
drwx------  2 james osboxes 4.0K Apr 26  2021 .ssh  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 Templates  
drwxr-xr-x  2 james osboxes 4.0K Apr 26  2021 Videos
```

OSBoxes group seems to be a VMWare/Virtualbox thing. This isn't really important at this time. I just wanted to point it out:
![[Pasted image 20230408034028.png]]
I should take note, however, of the shell-type: `rbash`
```
mindy@solidstate:~$ echo $SHELL  
/bin/rbash
```

Also known as `The Restricted Bash Shell`. Looking back at `/etc/passwd`, James has a regular bash shell. I'm able to escape using `-t "bash --noprofile"` option when logging into SSH however, now we are chrooted somewhere else:
![[Pasted image 20230408034648.png]]

## Kernel Version
`Linux version 4.9.0-3-686-pae (debian-kernel@lists.debian.org) (gcc version 6.3.0 20170516 (Debian 6.3.0-18) ) #1 SMP Debian 4.9.30-2+deb9u3 (2017-08-06) 32 bit`

![[Pasted image 20230408040548.png]]
A different vulnerability for once in these linux boxes. It's usually "pwnkit" or something similar but it doesn't appear to be particularly interesting as it exposes information for SSO.

Unless there's SSO in place on this box, I doubt this will be useful to me.

## Potential Exploit in Ptrace
https://github.com/jas502n/CVE-2019-13272

I will attempt to compile this exploit in a development environment. Fingers crossed...

## Custom Script found in /opt
![[Pasted image 20230408044040.png]]

#### tmp.py
```python
#!/usr/bin/env python
import os
import sys
try:
     os.system('rm -r /tmp/* ')
except:
     sys.exit()
```

I will check pspy to see if there's any funny processes being run by root
![[Pasted image 20230408045155.png]]

It appears to be running this. A reverse shell is in order.

![[Pasted image 20230408045411.png]]
![[Pasted image 20230408045930.png]]


