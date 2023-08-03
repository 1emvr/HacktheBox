10.10.10.60

## Enum
```bash
┌──(lemur㉿kali)-[~/htb/sense]  
└─$ sudo nmap 10.10.10.60 -p80,443 -sCV -T4 --min-rate 8000 -oA nmap/detailed-scan-allports-TCP -Pn  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-03 17:53 EDT  
Nmap scan report for 10.10.10.60  
Host is up (0.065s latency).  
  
PORT    STATE SERVICE  VERSION  
80/tcp  open  http     lighttpd 1.4.35  
|_http-server-header: lighttpd/1.4.35  
|_http-title: Did not follow redirect to https://10.10.10.60/  
443/tcp open  ssl/http lighttpd 1.4.35  
|_http-server-header: lighttpd/1.4.35  
|_ssl-date: TLS randomness does not represent time  
|_http-title: Login  
| ssl-cert: Subject: commonName=Common Name (eg, YOUR name)/organizationName=CompanyName/stateOrProvinceName=Somewhere/countryName=US  
| Not valid before: 2017-10-14T19:21:35  
|_Not valid after:  2023-04-06T19:21:35  
  
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 19.80 seconds
```

- Lighttpd 1.4.35 on both http and https. No common name except placeholder `Common Name`