10.10.10.162

## Nmap
```bash
┌──(lemur㉿kali)-[~/htb/mango]  
└─$ sudo nmap 10.10.10.162 -p22,80,443 -sCV -T4 --min-rate 8000 -oA nmap/initial-scan-allports-TCP                         
Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-03 19:46 EDT  
Nmap scan report for 10.10.10.162  
Host is up (0.067s latency).  
  
PORT    STATE SERVICE  VERSION  
22/tcp  open  ssh      OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)  
| ssh-hostkey:    
|   2048 a88fd96fa6e4ee56e3ef54546d560cf5 (RSA)  
|   256 6a1cba891eb0572ffe63e1617289b4cf (ECDSA)  
|_  256 9070fb6f38aedc3b0b316864b04e7dc9 (ED25519)  
80/tcp  open  http     Apache httpd 2.4.29 ((Ubuntu))  
|_http-server-header: Apache/2.4.29 (Ubuntu)  
|_http-title: 403 Forbidden  
443/tcp open  ssl/http Apache httpd 2.4.29 ((Ubuntu))  
| ssl-cert: Subject: commonName=staging-order.mango.htb/organizationName=Mango Prv Ltd./stateOrProvinceName=None/countryName=IN  
| Not valid before: 2019-09-27T14:21:19  
|_Not valid after:  2020-09-26T14:21:19  
|_http-server-header: Apache/2.4.29 (Ubuntu)  
| tls-alpn:    
|_  http/1.1  
|_ssl-date: TLS randomness does not represent time  
|_http-title: Mango | Search Base  
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 19.95 seconds
```

- OpenSSH 7.6p1
- Potentially Ubuntu 18.04 Bionic Beaver
- Apache httpd 2.4.29
- SSL cert entry for subdomain `staging-order.mango.htb`