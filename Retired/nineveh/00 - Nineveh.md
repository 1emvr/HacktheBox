/Nineveh is a medium, retired Linux box

## Info
```php
ATTACK: 10.10.16.3
TARGET: 10.10.10.43
```

## Enum
```bash
┌──(lemur㉿kali)-[~/htb/nineveh]  
└─$ sudo nmap 10.10.10.43 -p80,443 -sCV -T4 --min-rate 5000 -oA nmap/detailed-scan-allports-TCP  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-05 21:05 EDT  
Nmap scan report for 10.10.10.43  
Host is up (0.051s latency).  
  
PORT    STATE SERVICE  VERSION  
80/tcp  open  http     Apache httpd 2.4.18 ((Ubuntu))  
|_http-title: Site doesn't have a title (text/html).  
|_http-server-header: Apache/2.4.18 (Ubuntu)  
443/tcp open  ssl/http Apache httpd 2.4.18 ((Ubuntu))  
| ssl-cert: Subject: commonName=nineveh.htb/organizationName=HackTheBox Ltd/stateOrProvinceName=Athens/countryName=GR  
| Not valid before: 2017-07-01T15:03:30  
|_Not valid after:  2018-07-01T15:03:30  
|_ssl-date: TLS randomness does not represent time  
| tls-alpn:    
|_  http/1.1  
|_http-title: Site doesn't have a title (text/html).  
|_http-server-header: Apache/2.4.18 (Ubuntu)  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 19.60 seconds
```