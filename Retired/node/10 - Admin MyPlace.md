`"backup"` has been downloaded:
![[Pasted image 20230429013335.png]]

The file type is not recognized as any normal format:
![[Pasted image 20230429013542.png]]

Unsure of what this is I looked back to 0xdf and was introduced to the tool called `od`:
https://www.geeksforgeeks.org/od-command-linux-example/#
```
Od command in Linux is used to convert the content of input in different formats with octal format as the default format.

It can display output in a variety of other formats, including hexadecimal, decimal, and ASCII. It is useful for visualizing data that is not in a human-readable format, like the executable code of a program.
```

It might help to look for repeating patterns in this file:
````
cat myplace.backup | od -cvAnone -w1 | sort -bu | tr -d '\n' | tr -d ' '
````

`od by "character", -An "omit offset info", -o "display by 2-char byte", -n "numeric-sort"`

`sort, omitting blanks and "by unique value"`
`trim new-lines and spaces`

![[Pasted image 20230429015613.png]]

The character set does match base64. I thought it looked familiar at the beginning but I was unsure. I honestly can't believe this box rightnow....

![[Pasted image 20230429015833.png]]

\>:( really?

Now, there is a password on the file that needs cracked:
![[Pasted image 20230429020022.png]]
![[Pasted image 20230429020512.png]]
`magicword`

![[Pasted image 20230429020556.png]]

![[Pasted image 20230429021337.png]]
![[Pasted image 20230429021236.png]]

mmmyes, very good...

There is connectivity to MongoDB. 
```js
MongoClient.connect(url, function(error, db) {
  if (error || !db) {
    console.log('[!] Failed to connect to mongodb');
    return;
  }

  app.use(session({
    secret: 'the boundless tendency initiates the law.',
    cookie: { maxAge: 3600000 },
    resave: false,
    saveUninitialized: false
  }));

```

Do not show `is_admin` in `/api/users/latest.` This is why we didnt find him previously :
```js
app.get('/api/users/latest', function (req, res) {
    db.collection('users').find({ is_admin: false }).toArray(function (error, docs)
```

Database connection:
```js
const url         = 'mongodb://mark:5AYRft73VtFpc84k@localhost:27017/myplace?authMechanism=DEFAULT&authSource=myplace';
const backup_key  = '45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474';
```

`mark:5AYRft73VtFpc84k`. Potential for credential re-use:
![[Pasted image 20230429022559.png]]




