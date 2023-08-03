![[Pasted image 20230429023407.png]]
`mongorc.js, .dbshell` are potentially useful

![[Pasted image 20230429023530.png]]
`/usr/local/bin/backup (unknown SUID binary)`
`pkexec Linux4.10_to_5.1.17(CVE-2019-13272)`

![[Pasted image 20230429024014.png]]

```bash
╔══════════╣ Operative system
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation#kernel-exploits    

Linux version 4.4.0-93-generic (buildd@lgw01-03) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #116-Ubuntu SMP Fri Aug 11 21:17:51 UTC 2017                                                                                    
Distributor ID: Ubuntu 
Description:    Ubuntu 16.04.3 LTS 
Release:        16.04
Codename:       xenial
```

![[Pasted image 20230429030916.png]]
Two processes are running under `tom:` 
`/usr/bin/node /var/scheduler/app.js`
`/usr/bin/node /var/www/myplace/app.js`

user.txt is in Tom's directory:
![[Pasted image 20230429031055.png]]

The `/var/scheduler/app.js` is similar to the one we found credentials.
```js
const exec        = require('child_process').exec;  
const MongoClient = require('mongodb').MongoClient;  
const ObjectID    = require('mongodb').ObjectID;  
const url         = 'mongodb://mark:5AYRft73VtFpc84k@localhost:27017/scheduler?authMechanism=DEFAULT&authSource=scheduler';  
  
MongoClient.connect(url, function(error, db) {  
 if (error || !db) {  
   console.log('[!] Failed to connect to mongodb');  
   return;  
 }  
  
 setInterval(function () {  
   db.collection('tasks').find().toArray(function (error, docs) {  
     if (!error && docs) {  
       docs.forEach(function (doc) {  
         if (doc) {  
           console.log('Executing task ' + doc._id + '...');  
           exec(doc.cmd);  
           db.collection('tasks').deleteOne({ _id: new ObjectID(doc._id) });  
         }  
       });  
     }  
     else if (error) {  
       console.log('Something went wrong: ' + error);  
     }  
   });  
 }, 30000);  
  
});
```

The `setInterval` function runs commands every 30 seconds.
https://developer.mozilla.org/en-US/docs/Web/API/setInterval

I need to find out where these `tasks` are run from to potentially gain code execution. This apparently comes from something called `collection`, a part of `db`. This is all within Express, using MongoDB.

![[Pasted image 20230429033257.png]]
user mark is not allowed to list databases(?) but mongo allows for code execution

![[Pasted image 20230429034711.png]]

![[Pasted image 20230429035416.png]]
![[Pasted image 20230429040206.png]]
![[Pasted image 20230429040231.png]]




