arguments takes in up to 100 chars
![[Pasted image 20230429050430.png]]
```c
char *stpncpy(char dst[restrict .sz], const char *restrict src, size_t sz);`
```

read local file, along with error-checking
![[Pasted image 20230429051533.png]]
```c
FILE *fopen(const char *restrict pathname, const char *restrict mode);
```

Read the file into buffer to EOF. Calculate the size. Compare the buffer to input from cli, if the result is correct, display success, else laugh and quit...
![[Pasted image 20230429052532.png]]
```c
char *fgets(char s[restrict .size], int size, FILE *restrict stream);
size_t strcspn(const char *s, const char *reject);
int strncmp(const char s1[.n], const char s2[.n], size_t n);
```

and then there's this...
![[Pasted image 20230429052740.png]]
```c
    puts(
        "UEsDBDMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAcm9vdC50eHQBmQcAAgBBRQEIAEbBKBl0rFrayqfbwJ2YyHunnYq 1Za6G7XLo8C3RH/hu0fArpSvYauq4AUycRmLuWvPyJk3sF+HmNMciNHfFNLD3LdkGmgwSW8j50xlO6SWiH5qU1Edz340 bxpSlvaKvE4hnK/oan4wWPabhw/2rwaaJSXucU+pLgZorY67Q/Y6cfA2hLWJabgeobKjMy0njgC9c8cQDaVrfE/ZiS1S +rPgz/e2Pc3lgkQ+lAVBqjo4zmpQltgIXauCdhvlA1Pe/BXhPQBJab7NVF6Xm3207EfD3utbrcuUuQyF+rQhDCKsAEhq Q+Yyp1Tq2o6BvWJlhtWdts7rCubeoZPDBD6Mejp3XYkbSYYbzmgr1poNqnzT5XPiXnPwVqH1fG8OSO56xAvxx2mU2EP+ Yhgo4OAghyW1sgV8FxenV8p5c+u9bTBTz/7WlQDI0HUsFAOHnWBTYR4HTvyi8OPZXKmwsPAG1hrlcrNDqPrpsmxxmVR8 xSRbBDLSrH14pXYKPY/a4AZKO/GtVMULlrpbpIFqZ98zwmROFstmPl/cITNYWBlLtJ5AmsyCxBybfLxHdJKHMsK6Rp4M O+wXrd/EZNxM8lnW6XNOVgnFHMBsxJkqsYIWlO0MMyU9L1CL2RRwm2QvbdD8PLWA/jp1fuYUdWxvQWt7NjmXo7crC1dA 0BDPg5pVNxTrOc6lADp7xvGK/kP4F0eR+53a4dSL0b6xFnbL7WwRpcF+Ate/Ut22WlFrg9A8gqBC8Ub1SnBU2b93ElbG 9SFzno5TFmzXk3onbLaaEVZl9AKPA3sGEXZvVP+jueADQsokjJQwnzg1BRGFmqWbR6hxPagTVXBbQ+hytQdd26PCuhmR UyNjEIBFx/XqkSOfAhLI9+Oe4FH3hYqb1W6xfZcLhpBs4Vwh7t2WGrEnUm2/F+X/OD+s9xeYniyUrBTEaOWKEv2NOUZu dU6X2VOTX6QbHJryLdSU9XLHB+nEGeq+sdtifdUGeFLct+Ee2pgR/AsSexKmzW09cx865KuxKnR3yoC6roUBb30Ijm5v Quzg/RM71P5ldpCK70RemYniiNeluBfHwQLOxkDn/8MN0CEBr1eFzkCNdblNBVA7b9m7GjoEhQXOpOpSGrXwbiHHm5C7 Zn4kZtEy729ZOo71OVuT9i+4vCiWQLHrdxYkqiC7lmfCjMh9e05WEy1EBmPaFkYgxK2c6xWErsEv38++8xdqAcdEGXJB R2RT1TlxG/YlB4B7SwUem4xG6zJYi452F1klhkxloV6paNLWrcLwokdPJeCIrUbn+C9TesqoaaXASnictzNXUKzT905O FOcJwt7FbxyXk0z3FxD/tgtUHcFBLAQI/AzMDAQBjAG++IksAAAAA7QMAABgKAAAIAAsAAAAAAAAAIIC0gQAAAAByb29 0LnR4dAGZBwACAEFFAQgAUEsFBgAAAAABAAEAQQAAAB4EAAAAAA=="
        );
```

They all appear to be separate strings. None of them make any sense when run through `b64 -d`. There's some kind of cipher at play here.

There are several more of these blocks of b64 text and then the rest of the code:

![[Pasted image 20230429054641.png]]

It might be easier to run this like a debugger using `ltrace`.
![[Pasted image 20230429224121.png]]

We have an initial strcmp looking for -q, then 3 other strcmps looking for a certain other value. There's also 3 hashes in `/etc/myplace/keys:`
```
a01a6aa5aaf1d7729f35c8278daae30f8a988257144c003f8b12c5aec39bc508  
45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474  
3de811f4ab2b7543eaf45df611c2dd2541a5fc5af601772638b81dce6852d110
```

Running with the arguments `a b c`, replacing `b` with one of the keys seems to validate the application:
![[Pasted image 20230429225615.png]]

All of these encoded blocks are exactly the same... something's wrong here, and there's no actual ciphering/encryption functionality within this binary.

Looking back:
```c
fgets(<HASH>..., 1000, 0xa03f410)                    = 0xfff731ff  
strcspn(<HASH>..., "\n")                             = 64  
strcmp(<HASH>..., <HARDCODED_HASH>...) = 0  
strcpy(0xfff72238, "Validated access token")                                     = 0xfff72238  
printf(" %s[+]%s %s\n", "\033[32m", "\033[37m", "Validated access token" [+] Validated access token  
)        = 38  
fgets("45fac180e9eee72f4fd2d9386ea7033e"..., 1000, 0xa03f410)                    = 0xfff731ff  
strcspn("45fac180e9eee72f4fd2d9386ea7033e"..., "\n")                             = 64  
strcmp("a01a6aa5aaf1d7729f35c8278daae30f"..., "45fac180e9eee72f4fd2d9386ea7033e"...) = 1  
fgets("3de811f4ab2b7543eaf45df611c2dd25"..., 1000, 0xa03f410)                    = 0xfff731ff  
strcspn("3de811f4ab2b7543eaf45df611c2dd25"..., "\n")                             = 64  
strcmp("a01a6aa5aaf1d7729f35c8278daae30f"..., "3de811f4ab2b7543eaf45df611c2dd25"...) = 1  
fgets("\n", 1000, 0xa03f410)                                                     = 0xfff731ff  
strcspn("\n", "\n")                                                              = 0  
strcmp("a01a6aa5aaf1d7729f35c8278daae30f"..., "")                                = 1  
fgets(nil, 1000, 0xa03f410)                                                      = 0  
strstr("/root", "..")                                                            = nil  
strstr("/root", "/root")                                                         = "/root"
```

Potential for BOF. Checks seem to indicate 507 chars is the limit:
![[Pasted image 20230429234324.png]]

and I can't get the thing to fucking segfault. amazing