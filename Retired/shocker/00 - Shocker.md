Shocker is an easy, retired Linux box
target=10.10.10.56
attacker=10.10.16.3

## Enumeration
```bash
┌──(lemur㉿kali)-[~/htb/shocker]  
└─$ sudo nmap 10.10.10.56 -p80,2222 -sCV -T4 --min-rate 5000 -oA nmap/detailed-scan-allports-TCP  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-05 17:32 EDT  
Nmap scan report for 10.10.10.56  
Host is up (0.058s latency).  
  
PORT     STATE SERVICE VERSION  
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))  
|_http-server-header: Apache/2.4.18 (Ubuntu)  
|_http-title: Site doesn't have a title (text/html).  
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)  
| ssh-hostkey:    
|   2048 c4f8ade8f80477decf150d630a187e49 (RSA)  
|   256 228fb197bf0f1708fc7e2c8fe9773a48 (ECDSA)  
|_  256 e6ac27a3b5a9f1123c34a55d5beb3de9 (ED25519)  
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 11.12 seconds
```

