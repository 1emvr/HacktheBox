A retired, medium Linux box
10.10.10.51

## Enum
```bash
┌──(lemur㉿kali)-[~/htb/solidstate]  
└─$ sudo nmap 10.10.10.51 -p- -T4 --min-rate 5000 -oA nmap/initial-scan-allports-TCP -Pn  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-08 00:33 EDT  
Nmap scan report for 10.10.10.51  
Host is up (0.028s latency).  
Not shown: 65520 closed tcp ports (reset)  
PORT      STATE    SERVICE  
22/tcp    open     ssh  
25/tcp    open     smtp  
80/tcp    open     http  
110/tcp   open     pop3  
119/tcp   open     nntp  
4555/tcp  open     rsip  
15973/tcp filtered unknown  
17496/tcp filtered unknown  
20323/tcp filtered unknown  
21121/tcp filtered unknown  
30179/tcp filtered unknown  
30596/tcp filtered unknown  
45658/tcp filtered unknown  
54145/tcp filtered unknown  
56627/tcp filtered unknown  
  
Nmap done: 1 IP address (1 host up) scanned in 39.46 seconds
```

## Common Ports
```bash
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4p1 Debian 10+deb9u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 770084f578b9c7d354cf712e0d526d8b (RSA)
|   256 78b83af660190691f553921d3f48ed53 (ECDSA)
|_  256 e445e9ed074d7369435a12709dc4af76 (ED25519)
25/tcp   open  smtp    JAMES smtpd 2.3.2
|_smtp-commands: solidstate Hello nmap.scanme.org (10.10.16.2 [10.10.16.2])
80/tcp   open  http    Apache httpd 2.4.25 ((Debian))
|_http-title: Home - Solid State Security
|_http-server-header: Apache/2.4.25 (Debian)
110/tcp  open  pop3    JAMES pop3d 2.3.2
119/tcp  open  nntp    JAMES nntpd (posting ok)
4555/tcp open  rsip?
| fingerprint-strings: 
|   GenericLines: 
|     JAMES Remote Administration Tool 2.3.2
|     Please enter your login and password
|     Login id:
|     Password:
|     Login failed for 
|_    Login id:
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port4555-TCP:V=7.93%I=7%D=4/8%Time=6430EF1B%P=x86_64-pc-linux-gnu%r(Gen
SF:ericLines,7C,"JAMES\x20Remote\x20Administration\x20Tool\x202\.3\.2\nPle
SF:ase\x20enter\x20your\x20login\x20and\x20password\nLogin\x20id:\nPasswor
SF:d:\nLogin\x20failed\x20for\x20\nLogin\x20id:\n");
Service Info: Host: solidstate; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Apr  8 00:39:49 2023 -- 1 IP address (1 host up) scanned in 262.01 seconds
```

`JAMES` appears as an apparent name for email services, possible user.

## Higher Ports
```bash
┌──(lemur㉿kali)-[~/htb/solidstate]  
└─$ sudo nmap 10.10.10.51 -p15973,17496,20323,21121,30179,30596,45658,54145,56627 -sCV -T4 --min-rate 5000 -oA nmap/detailed-scan-higherports-TCP -Pn  
[sudo] password for lemur:    
Starting Nmap 7.93 ( https://nmap.org ) at 2023-04-08 01:14 EDT  
Nmap scan report for 10.10.10.51  
Host is up (0.087s latency).  
  
PORT      STATE  SERVICE VERSION  
15973/tcp closed unknown  
17496/tcp closed unknown  
20323/tcp closed unknown  
21121/tcp closed unknown  
30179/tcp closed unknown  
30596/tcp closed unknown  
45658/tcp closed unknown  
54145/tcp closed unknown  
56627/tcp closed unknown  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 0.64 seconds
```

Not sure why these higher ports show up in the first scan because they're apparently all closed.

## RSIP - Realm-Specific IP - 4555
```
An experimental [IETF] framework and protocol intended as an alternative to [network address translation] (NAT) in which the end-to-end integrity of packets is maintained.

RSIP lets a host borrow one or more [IP addresses] (and UDP/TCP port) from one or more RSIP gateways, by leasing (usually public) IP addresses and ports to RSIP hosts located in other (usually private) addressing realms.
```

```
JAMES Remote Administration Tool 2.3.2
    Please enter your login and password
```

## Network News Transfer Protocol - 119
```
The **Network News Transfer Protocol** (**NNTP**) is an application [protocol] used for transporting [Usenet] news articles (_netnews_) between [news servers], and for reading/posting articles by the end user client applications.
```

