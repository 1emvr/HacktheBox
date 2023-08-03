![[Pasted image 20230502054824.png]]

```
Sites to be tested: ini.php, info.php, listfiles.php, phpinfo.php
```

![[Pasted image 20230502055010.png]]

```
Warning: include(test.php): failed to open stream: No such file or directory in /usr/local/www/apache24/data/browse.php on line 2  
  
Warning: include(): Failed opening 'test.php' for inclusion (include_path='.:/usr/local/www/apache24/data') in /usr/local/www/apache24/data/browse.php on line 2
```

browse.php and test.php are included in `/usr/local/www/apache24/data`. Path traversal could be possible.

![[Pasted image 20230502055930.png]]
Reading `/etc/passwd`. Trying to read browse.php:

![[Pasted image 20230502060027.png]]

## ini.php
![[Pasted image 20230502060304.png]]

## info.php
![[Pasted image 20230502060340.png]]
`FreeBSD Poison 11.1-RELEASE FreeBSD 11.1-RELEASE #0 r321309: Fri Jul 21 02:08:28 UTC 2017`

## listfiles.php
![[Pasted image 20230502060417.png]]
`Array ( [0] => . [1] => .. [2] => browse.php [3] => index.php [4] => info.php [5] => ini.php [6] => listfiles.php [7] => phpinfo.php [8] => pwdbackup.txt )`

There is a password backup text file on the system.

## phpinfo.php
![[Pasted image 20230502060448.png]]`PHP Version 5.6.32`
``

## pwdbackup.txt
![[Pasted image 20230502061022.png]]
```
This password is secure, it's encoded atleast 13 times.. what could go wrong really.. 

Vm0wd2QyUXlVWGxWV0d4WFlURndVRlpzWkZOalJsWjBUVlpPV0ZKc2JETlhhMk0xVmpKS1IySkVU bGhoTVVwVVZtcEdZV015U2tWVQpiR2hvVFZWd1ZWWnRjRWRUTWxKSVZtdGtXQXBpUm5CUFdWZDBS bVZHV25SalJYUlVUVlUxU1ZadGRGZFZaM0JwVmxad1dWWnRNVFJqCk1EQjRXa1prWVZKR1NsVlVW M040VGtaa2NtRkdaR2hWV0VKVVdXeGFTMVZHWkZoTlZGSlRDazFFUWpSV01qVlRZVEZLYzJOSVRs WmkKV0doNlZHeGFZVk5IVWtsVWJXaFdWMFZLVlZkWGVHRlRNbEY0VjI1U2ExSXdXbUZEYkZwelYy eG9XR0V4Y0hKWFZscExVakZPZEZKcwpaR2dLWVRCWk1GWkhkR0ZaVms1R1RsWmtZVkl5YUZkV01G WkxWbFprV0dWSFJsUk5WbkJZVmpKMGExWnRSWHBWYmtKRVlYcEdlVmxyClVsTldNREZ4Vm10NFYw MXVUak5hVm1SSFVqRldjd3BqUjJ0TFZXMDFRMkl4WkhOYVJGSlhUV3hLUjFSc1dtdFpWa2w1WVVa T1YwMUcKV2t4V2JGcHJWMGRXU0dSSGJFNWlSWEEyVmpKMFlXRXhXblJTV0hCV1ltczFSVmxzVm5k WFJsbDVDbVJIT1ZkTlJFWjRWbTEwTkZkRwpXbk5qUlhoV1lXdGFVRmw2UmxkamQzQlhZa2RPVEZk WGRHOVJiVlp6VjI1U2FsSlhVbGRVVmxwelRrWlplVTVWT1ZwV2EydzFXVlZhCmExWXdNVWNLVjJ0 NFYySkdjR2hhUlZWNFZsWkdkR1JGTldoTmJtTjNWbXBLTUdJeFVYaGlSbVJWWVRKb1YxbHJWVEZT Vm14elZteHcKVG1KR2NEQkRiVlpJVDFaa2FWWllRa3BYVmxadlpERlpkd3BOV0VaVFlrZG9hRlZz WkZOWFJsWnhVbXM1YW1RelFtaFZiVEZQVkVaawpXR1ZHV210TmJFWTBWakowVjFVeVNraFZiRnBW VmpOU00xcFhlRmRYUjFaSFdrWldhVkpZUW1GV2EyUXdDazVHU2tkalJGbExWRlZTCmMxSkdjRFpO Ukd4RVdub3dPVU5uUFQwSwo=
```

Removing whitespace and decoding:
![[Pasted image 20230502061659.png]]
`Charix!2#4%6&8(0`

## /etc/passwd
```
# $FreeBSD: releng/11.1/etc/master.passwd 299365 2016-05-10 12:47:36Z bcr $ # 
root:*:0:0:Charlie &:/root:/bin/csh toor:*:0:0:Bourne-again Superuser:/root: 
daemon:*:1:1:Owner of many system processes:/root:/usr/sbin/nologin 
operator:*:2:5:System &:/:/usr/sbin/nologin 
bin:*:3:7:Binaries Commands and Source:/:/usr/sbin/nologin 
tty:*:4:65533:Tty Sandbox:/:/usr/sbin/nologin 
kmem:*:5:65533:KMem Sandbox:/:/usr/sbin/nologin 
games:*:7:13:Games pseudo-user:/:/usr/sbin/nologin 
news:*:8:8:News Subsystem:/:/usr/sbin/nologin 
man:*:9:9:Mister Man Pages:/usr/share/man:/usr/sbin/nologin 
sshd:*:22:22:Secure Shell Daemon:/var/empty:/usr/sbin/nologin 
smmsp:*:25:25:Sendmail Submission User:/var/spool/clientmqueue:/usr/sbin/nologin 
mailnull:*:26:26:Sendmail Default User:/var/spool/mqueue:/usr/sbin/nologin 
bind:*:53:53:Bind Sandbox:/:/usr/sbin/nologin 
unbound:*:59:59:Unbound DNS Resolver:/var/unbound:/usr/sbin/nologin 
proxy:*:62:62:Packet Filter pseudo-user:/nonexistent:/usr/sbin/nologin 
_pflogd:*:64:64:pflogd privsep user:/var/empty:/usr/sbin/nologin 
_dhcp:*:65:65:dhcp programs:/var/empty:/usr/sbin/nologin 
uucp:*:66:66:UUCP pseudo-user:/var/spool/uucppublic:/usr/local/libexec/uucp/uucico 
pop:*:68:6:Post Office Owner:/nonexistent:/usr/sbin/nologin 
auditdistd:*:78:77:Auditdistd unprivileged user:/var/empty:/usr/sbin/nologin 
www:*:80:80:World Wide Web Owner:/nonexistent:/usr/sbin/nologin 
_ypldap:*:160:160:YP LDAP unprivileged user:/var/empty:/usr/sbin/nologin 
hast:*:845:845:HAST unprivileged user:/var/empty:/usr/sbin/nologin 
nobody:*:65534:65534:Unprivileged user:/nonexistent:/usr/sbin/nologin 
_tss:*:601:601:TrouSerS user:/var/empty:/usr/sbin/nologin 
messagebus:*:556:556:D-BUS Daemon User:/nonexistent:/usr/sbin/nologin 
avahi:*:558:558:Avahi Daemon User:/nonexistent:/usr/sbin/nologin 
cups:*:193:193:Cups Owner:/nonexistent:/usr/sbin/nologin 
charix:*:1001:1001:charix:/home/charix:/bin/csh 
```

![[Pasted image 20230502062631.png]]

`charix:Charix!2#4%6&8(0`

## intended method

When LFI is available using the `include()` method we have potential for `Apache log poisoning`. 

![[Pasted image 20230502170412.png]]

## httpd-error.log
![[Pasted image 20230502170516.png]]

## httpd-access.log
![[Pasted image 20230502170545.png]]

Since we have access to files through parameters, as seen in access log, I likely have log poisoning available to me. Intercepting the requests, I can include a php one-liner into the user-agent field of the request, giving RCE.

![[Pasted image 20230502171026.png]]
![[Pasted image 20230502171438.png]]
![[Pasted image 20230502171616.png]]
I simply connect with a nc session using this method, then drop it as I already have the more stable SSH access instead.