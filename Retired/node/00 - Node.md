## 10.10.10.58

## Enum
```bash
┌──(lemur㉿kali)-[~/htb/node]  
└─$ sudo nmap 10.10.10.58 -p22,3000 -sCV -T4 -min-rate 5000 -oA nmap/detailed-scan-allports-TCP  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-28 23:44 EDT  
Nmap scan report for 10.10.10.58  
Host is up (0.026s latency).  
  
PORT     STATE SERVICE         VERSION  
22/tcp   open  ssh             OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)  
| ssh-hostkey:    
|   2048 dc5e34a625db43eceb40f4967b8ed1da (RSA)  
|   256 6c8e5e5f4fd5417d1895d1dc2e3fe59c (ECDSA)  
|_  256 d878b85d85ffad7be6e2b5da1e526236 (ED25519)  
3000/tcp open  hadoop-datanode Apache Hadoop  
| hadoop-tasktracker-info:    
|_  Logs: /login  
|_http-title: MyPlace  
| hadoop-datanode-info:    
|_  Logs: /login  
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 17.01 seconds
```

- OpenSSH 7.2p2 Ubuntu
- Apache Hadoop. "tasktracker" info and "datanode" info

