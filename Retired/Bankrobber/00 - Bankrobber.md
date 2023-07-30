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

There seems to be SQL-Injection present in the user database lookup, although I have yet to go any further.
```

`admin:Hopelessromantic`


