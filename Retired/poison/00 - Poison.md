10.10.10.84

## Enum
```bash
┌──(lemur㉿kali)-[~/htb/poison]  
└─$ sudo nmap 10.10.10.84 -p22,80 -sCV -T4 --min-rate 5000 -oA nmap/detailed-scan-allports-TCP  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-02 05:42 EDT  
Nmap scan report for 10.10.10.84  
Host is up (0.061s latency).  
  
PORT   STATE SERVICE VERSION  
22/tcp open  ssh     OpenSSH 7.2 (FreeBSD 20161230; protocol 2.0)  
| ssh-hostkey:    
|   2048 e33b7d3c8f4b8cf9cd7fd23ace2dffbb (RSA)  
|   256 4ce8c602bdfc83ffc98001547d228172 (ECDSA)  
|_  256 0b8fd57185901385618beb34135f943b (ED25519)  
80/tcp open  http    Apache httpd 2.4.29 ((FreeBSD) PHP/5.6.32)  
|_http-server-header: Apache/2.4.29 (FreeBSD) PHP/5.6.32  
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).  
Service Info: OS: FreeBSD; CPE: cpe:/o:freebsd:freebsd  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 10.90 seconds
```

- OpenSSH 7.2 - Potentially FreeBSD 11.1
- Apache 2.4.29 running PHP 5.6.32

```
Potential vulnerabilities:
https://www.rapid7.com/db/vulnerabilities/freebsd-vid-e4644df8-e7da-11e5-829d-c80aa9043978/
```

