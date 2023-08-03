#### Apache/2.4.18
![[Pasted image 20230405210918.png]]
![[Pasted image 20230405210740.png]]

`Email Address admin@nineveh.htb`
`Common Name nineveh.htb`

![[Pasted image 20230405221516.png]]

![[Pasted image 20230405212327.png]]
## /db/index.php
![[Pasted image 20230405212418.png]]
`**Warning**: rand() expects parameter 2 to be integer, float given in **/var/www/ssl/db/index.php** on line 114`

`phpLiteAdmin v1.9`
 Noticing most of these exploits interact with MySQL I quickly scanned for it on port `3306`

![[Pasted image 20230405214314.png]]

## PhpLiteAdmin
No real interesting unauthenticated exploits and since there is no username field, only password, and there's very little information to go off of, it makes sense to try brute forcing.

I found the password to be `password123`
![[Pasted image 20230405223513.png]]

Seems to display the local file. Will test for LFI later.
![[Pasted image 20230406143220.png]]

PhpLiteAdmin uses SQLite syntax:
- `sqlite_version() 3.11.0`

LFI is required in order to exploit this vulnerability but it doesn't seem to be available directly. I will leave a php payload in place for now. Reference:
https://www.exploit-db.com/exploits/24044

Database lemur.php:
`CREATE TABLE 'test_table' ('exploit' TEXT default '<?php phpinfo()?>')`

## /department

#### Type Juggling and interfering with password comparison
https://medium.com/swlh/php-type-juggling-vulnerabilities-3e28c4ed5c09
https://cybernetgen.com/auth-bypass-with-php-type-juggling/

These articles explain why passing an array for password will completely fuck-up the strcmp for passwords and then return NULL, completing the statement that is used for authentication.

![[Pasted image 20230406152604.png]]
![[Pasted image 20230406152806.png]]
`http://nineveh.htb/department/manage.php?notes=files/ninevehNotes.txt`

```
Have you fixed the login page yet! hardcoded username and password is really bad idea!

check your serect folder to get in! figure it out! this is your challenge
Improve the db interface.

	~amrois
```

Testing for LFI only seems to work when the base file name is included. It will not work trying to directly start from `../` base directory, so I had to include the note from the start.

If I try with simply `../../../../../etc/passwd` it tells me that `No Note is selected`, which means that it wants a note included

![[Pasted image 20230406160508.png]]

Also, the file extension for notes seems to break the LFI for some reason, so it needs to be removed.

![[Pasted image 20230406155225.png]]
I instantly get a hit. 
![[Pasted image 20230406155258.png]]
![[Pasted image 20230406155622.png]]
There is one single user, `amrois`

I should be able to trigger my php database code stored in `/db/`. I will have to find out where it's saved. :^)

![[Pasted image 20230406162057.png]]
Now I'll try something more interesting:
![[Pasted image 20230406162550.png]]
![[Pasted image 20230406162637.png]]
...didn't work. I can try something a bit simpler.
![[Pasted image 20230406164306.png]]

Using the `$_REQUEST` parameter for system instead of the common `$_GET` parameter because GET simply gets the content while REQUEST will process data.
![[Pasted image 20230406170349.png]]
Changed `?cmd=` to download a meterpreter implant to `/tmp`, chmod it to become executable and run it.
![[Pasted image 20230406180254.png]]

