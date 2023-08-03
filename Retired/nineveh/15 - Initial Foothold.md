`Linux nineveh 4.4.0-62-generic #83-Ubuntu SMP Wed Jan 18 14:10:15 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux`

## Port knocking script
![[Pasted image 20230406183818.png]]

## In-Memory Credentials (return later)
![[Pasted image 20230406184346.png]]

## Vulnerable to PwnKit:
![[Pasted image 20230406184737.png]]
however, this exploit crashes the system.

## Other exploits
![[Pasted image 20230406192356.png]]

#2 will not work as it requires X11
#3 seems the most vialbe. It's a kernel exploit so there's potential for system failure.

https://www.exploit-db.com/exploits/45010

Obtained root with kernel exploit `CVE-2017-16995`

```
The vulnerability allows for arbitrary read/write access to the linux kernel, bypassing SMEP/SMAP
```
https://www.openwall.com/lists/oss-security/2017/12/21/2