10.10.10.140

## Nmap
```bash
┌──(lemur㉿kali)-[~/htb/swagshop]  
└─$ sudo nmap 10.10.10.140 -p22,80 -sCV -T4 --min-rate 8000 -oA nmap/initial-scan-allports-TCP  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-04 21:44 EDT  
Nmap scan report for 10.10.10.140  
Host is up (0.051s latency).  
  
PORT   STATE SERVICE VERSION  
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)  
| ssh-hostkey:    
|   2048 b6552bd24e8fa3817261379a12f624ec (RSA)  
|   256 2e30007a92f0893059c17756ad51c0ba (ECDSA)  
|_  256 4c50d5f270c5fdc4b2f0bc4220326434 (ED25519)  
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))  
|_http-title: Did not follow redirect to http://swagshop.htb/  
|_http-server-header: Apache/2.4.18 (Ubuntu)  
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 10.83 seconds
```

- OpenSSH 7.2p2 Ubuntu, possilby indicating Ubuntu 16.04 Xenial, one of my favorites
- Apache 2.4.18 Potential Security Issues in 14.04 and 16.04:
	https://ubuntu.com/security/notices/USN-4994-2

