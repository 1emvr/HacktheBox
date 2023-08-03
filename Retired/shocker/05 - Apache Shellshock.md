![[Pasted image 20230405173440.png]]
![[Pasted image 20230405174314.png]]

![[Pasted image 20230405181924.png]]
Using the `-f` option in feroxbuster appends the trailing `/` to the end of requests, which changes the outcome of directory searching.

```
http://shocker.htb/cgi-bin/   
http://shocker.htb/icons/   
http://shocker.htb/icons/small/
```

![[Pasted image 20230405182149.png]]

There is also a `/server-status` not previously mentioned. They all a code of return `403 Forbidden`.

![[Pasted image 20230405182857.png]]
The `/cgi-bin` is particularly interesting. Scanning the directory reveals a script named `user.sh`

![[Pasted image 20230405183305.png]]
Visiting the link it provides a download of the output.

![[Pasted image 20230405183835.png]]
Looking at response headers shows that the type is `x-sh`, which is not a typical format that firefox can handle. The user.sh I've downloaded shows a `content-type` header as if the script were trying to append this to the header but fails, putting it in the body, instead.

The rest of the output appears to be the `uptime` command.
![[Pasted image 20230405184153.png]]

```bash
https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/cgi
#shellshock

Bash can also be used to run commands passed to it by applications and it is this feature that the vulnerability affects. One type of command that can be sent to Bash allows environment variables to be set. Environment variables are dynamic, named values that affect the way processes are run on a computer. The vulnerability lies in the fact that an **attacker can tack-on malicious code to the environment variable, which will run once the variable is received**.

Exploiting this vulnerability the **page could throw an error**.

You could **find** this vulnerability noticing that it is using an **old Apache version** and **cgi_mod** (with cgi folder) or using **nikto**.
```

![[Pasted image 20230405185726.png]]
https://www.exploit-db.com/exploits/34900

![[Pasted image 20230405190054.png]]

![[Pasted image 20230405190627.png]]

![[Pasted image 20230405191315.png]]
![[Pasted image 20230405191608.png]]

