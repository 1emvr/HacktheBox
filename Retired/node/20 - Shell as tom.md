![[Pasted image 20230429041256.png]]
Tom is part of the `adm` group and the `admin` group seems to be a custom one.

![[Pasted image 20230429041657.png]]
![[Pasted image 20230429041944.png]]

```js
app.get('/api/admin/backup', function (req, res) {
    if (req.session.user && req.session.user.is_admin) {
      var proc = spawn('/usr/local/bin/backup', ['-q', backup_key, __dirname ]);
      var backup = '';

      proc.on("exit", function(exitCode) {
        res.header("Content-Type", "text/plain");
        res.header("Content-Disposition", "attachment; filename=myplace.backup");
        res.send(backup);
      });

      proc.stdout.on("data", function(chunk) {
        backup += chunk;
      });

      proc.stdout.on("end", function() {
      });
    }
    else {
      res.send({
        authenticated: false
      });
    }
  });
```

This part of the app seems to use this binary. a backup key and directory is supplied as arguments.

`__dirname is **an environment variable that tells you the absolute path of the directory containing the currently executing file**.`

So, this script takes the backup key and executes within the current directory. This app is located in `/var/www/myplace/app.js`. I exfiltrate the binary for reverse engineering.