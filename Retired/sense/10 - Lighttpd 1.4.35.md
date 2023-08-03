## Potential attack vectors (option)
![[Pasted image 20230503180446.png]]
https://www.tenable.com/plugins/was/112358

```
#### Description

Multiple directory traversal vulnerabilities in (1) mod_evhost and (2) mod_simple_vhost in lighttpd before 1.4.35 allow remote attackers to read arbitrary files via a .. (dot dot) in the host name, related to request_check_hostname.
```

There's not enough information to determine what is here, so I need to resort to deep scanning of directories, files available as well as nikto scanning.

![[Pasted image 20230503183402.png]]

A `system-users.txt` was also found.
```
####Support ticket###

Please create the following user


username: Rohit
password: company defaults
```

Company defaults could be anything. I really hate making goddamn wordlists and doing bruteforcing but it might be something I have to do... lame af. But it could also be `pfsense defaults` which I already know as `pfsense` for the password.

![[Pasted image 20230503184118.png]]
Damn... dodged a bullet.

