![[Pasted image 20230502010141.png]]
Both the `http and https` sites appear to be the same. The site is running with php.

![[Pasted image 20230502011013.png]]
There could be some information within this jpeg but it seems to be password protected

## Feroxbuster
![[Pasted image 20230502015003.png]]
```
200      GET       38c https://valentine.htb/  
200      GET       38c https://valentine.htb/index  
301      GET      314c https://valentine.htb/dev => https://valentine.htb/dev/  
200      GET      554c https://valentine.htb/encode  
200      GET      552c https://valentine.htb/decode  
200      GET   275344c https://valentine.htb/omg  
403      GET      295c https://valentine.htb/server-status
```

![[Pasted image 20230502020142.png]]

## hype_key
![[Pasted image 20230502020201.png]]
![[Pasted image 20230502021149.png]]
```
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,AEB88C140F69BF2074788DE24AE48D46
```

## note.txt
```
To do:

1) Coffee.
2) Research.
3) Fix decoder/encoder before going live.
4) Make sure encoding/decoding is only done client-side.
5) Don't use the decoder/encoder until any of this is done.
6) Find a better way to take notes.
```

## decoder
![[Pasted image 20230502021612.png]]

Potential OpenSSL vulnerability:
![[Pasted image 20230502022532.png]]

![[Pasted image 20230502034136.png]]
![[Pasted image 20230502034203.png]]
`heartbleedbelievethehype`