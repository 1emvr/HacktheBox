10.10.10.143

## Nmap
```bash
┌──(lemur㉿kali)-[~/htb/jarvis]  
└─$ sudo nmap 10.10.10.143 -p22,80 -T4 -sCV --min-rate 8000 -oA nmap/initial-scan-allports-TCP -Pn  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-03 23:06 EDT  
Nmap scan report for 10.10.10.143  
Host is up (0.059s latency).  
  
PORT   STATE SERVICE VERSION  
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)  
| ssh-hostkey:    
|   2048 03f34e22363e3b813079ed4967651667 (RSA)  
|   256 25d808a84d6de8d2f8434a2c20c85af6 (ECDSA)  
|_  256 77d4ae1fb0be151ff8cdc8153ac369e1 (ED25519)  
80/tcp open  http    Apache httpd 2.4.25 ((Debian))  
|_http-server-header: Apache/2.4.25 (Debian)  
| http-cookie-flags:    
|   /:    
|     PHPSESSID:    
|_      httponly flag not set  
|_http-title: Stark Hotel  
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 10.53 seconds
```

- OpenSSH 7.4p1, potentially Debian 10 (Buster)
- Apache 2.4.25

