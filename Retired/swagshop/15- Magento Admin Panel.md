![[Pasted image 20230505002753.png]]
There appears to be a RCE exploit that makes POST requests to an AJAX endpoint, calling on php's `system()` function in some odd way.

https://www.exploit-db.com/exploits/37811
However, Python fucked everything up for me. I'm going to kms soon. 
*****

![[Pasted image 20230505022955.png]]

There are 2 separate login fields, trying to confuse the script (and it worked).
`mechanize._form_controls.AmbiguityError: more than one control matching name 'login[username]'`

Changing the form control and setting up a proxy helped fix the issue (with a bit of experience and plenty of Googling):
![[Pasted image 20230505023859.png]]
![[Pasted image 20230505023933.png]]

![[Pasted image 20230505024001.png]]


****
