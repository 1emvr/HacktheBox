![[Pasted image 20230405200230.png]]
Because this site is using DNS, there's potentially different subdomains or Vhosts.

```bash
┌──(lemur㉿kali)-[~/htb/cronos]  
└─$ dig cronos.htb @10.10.10.13  
  
; <<>> DiG 9.18.12-1-Debian <<>> cronos.htb @10.10.10.13  
;; global options: +cmd  
;; Got answer:  
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 60906  
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 2  
  
;; OPT PSEUDOSECTION:  
; EDNS: version: 0, flags:; udp: 4096  
;; QUESTION SECTION:  
;cronos.htb.                    IN      A  
  
;; ANSWER SECTION:  
cronos.htb.             604800  IN      A       10.10.10.13  
  
;; AUTHORITY SECTION:  
cronos.htb.             604800  IN      NS      ns1.cronos.htb.  
  
;; ADDITIONAL SECTION:  
ns1.cronos.htb.         604800  IN      A       10.10.10.13  
  
;; Query time: 48 msec  
;; SERVER: 10.10.10.13#53(10.10.10.13) (UDP)  
;; WHEN: Wed Apr 05 20:06:23 EDT 2023  
;; MSG SIZE  rcvd: 89
```

I will add these names to `/etc/hosts`
```
┌──(lemur㉿kali)-[~/htb/cronos]  
└─$ dig axfr cronos.htb @ns1.cronos.htb  
  
; <<>> DiG 9.18.12-1-Debian <<>> axfr cronos.htb @ns1.cronos.htb  
;; global options: +cmd  
cronos.htb.             604800  IN      SOA     cronos.htb. admin.cronos.htb. 3 604800 86400 2419200 604800  
cronos.htb.             604800  IN      NS      ns1.cronos.htb.  
cronos.htb.             604800  IN      A       10.10.10.13  
admin.cronos.htb.       604800  IN      A       10.10.10.13  
ns1.cronos.htb.         604800  IN      A       10.10.10.13  
www.cronos.htb.         604800  IN      A       10.10.10.13  
cronos.htb.             604800  IN      SOA     cronos.htb. admin.cronos.htb. 3 604800 86400 2419200 604800  
;; Query time: 164 msec  
;; SERVER: 10.10.10.13#53(ns1.cronos.htb) (TCP)  
;; WHEN: Wed Apr 05 20:08:17 EDT 2023  
;; XFR size: 7 records (messages 1, bytes 203)
```

