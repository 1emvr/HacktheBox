![[Pasted image 20230502215318.png]]

![[Pasted image 20230502215927.png]]
```
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: netadm  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: netcfg  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: dhcpserv  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: ikeuser  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: adm  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: dladm  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: lp  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: root  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: nobody  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: noaccess  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: nobody4  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: sammy  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: pkg5srv  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: sunny  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: bin  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: daemon  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: unknown  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: smmsp  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: aiuser  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: openldap  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: sys  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: ftp  
[+] 10.10.10.76:79        - 10.10.10.76:79 - Found user: webservd  
^C[*] 10.10.10.76:79        - Caught interrupt from the console...
```

![[Pasted image 20230503171039.png]]
Apparently, sammy and sunny are logged in via SSH. This very well could be a case of `password reuse` and a `password complexity issue` which I simply don't understand.

![[Pasted image 20230503171308.png]]
`sunny:sunday`

