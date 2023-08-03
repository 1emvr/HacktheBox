Cronos is a medium, retired Linux box

## Info
```
TARGET: 10.10.10.13
ATTACK: 10.10.16.3
```

## Enumeration
```bash
┌──(lemur㉿kali)-[~/htb/cronos]  
└─$ sudo nmap 10.10.10.13 -p22,53,80 -sCV -T4 --min-rate 5000 -oA nmap/detailed-scan-allports-TCP  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-05 20:00 EDT  
Nmap scan report for 10.10.10.13  
Host is up (0.057s latency).  
  
PORT   STATE SERVICE VERSION  
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)  
| ssh-hostkey:    
|   2048 18b973826f26c7788f1b3988d802cee8 (RSA)  
|   256 1ae606a6050bbb4192b028bf7fe5963b (ECDSA)  
|_  256 1a0ee7ba00cc020104cda3a93f5e2220 (ED25519)  
53/tcp open  domain  ISC BIND 9.10.3-P4 (Ubuntu Linux)  
| dns-nsid:    
|_  bind.version: 9.10.3-P4-Ubuntu  
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))  
|_http-server-header: Apache/2.4.18 (Ubuntu)  
|_http-title: Apache2 Ubuntu Default Page: It works  
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 16.18 seconds
```



