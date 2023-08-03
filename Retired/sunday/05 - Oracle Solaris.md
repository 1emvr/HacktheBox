![[Pasted image 20230502210849.png]]

The login form takes a username, then a password upon entering. A generic `UNIX` host type from the nmap scan and Google accordingly may indicate that the system is running an OS called `Oracle Solaris`, originally owned/created by `Sun Microsystems.` This distribution was actually discontinued in January 2010.

`Oracle Solaris integrates software-defined networking and built-in virtualization with a proven enterprise-class operating system to provide an efficient, secure and compliant, simple, open, and affordable solution for deploying your enterprise-grade clouds`

## Login request
![[Pasted image 20230503170027.png]]

The accepted format is json. It makes a GET request to API endpoint `/solaris/api/login`.


