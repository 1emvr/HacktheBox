`Version: JAMES smtpd 2.3.2`

## Arbitrary File Write

![[Pasted image 20230408020602.png]]
![[Pasted image 20230408021741.png]]

The module successfully logged into the server. However, the exploit did not work, but I now know that the credentials of `root:root` will work, so I log into the administration tool manually using netcat.

![[Pasted image 20230408023224.png]]
![[Pasted image 20230408023338.png]]

```
listusers  
Existing accounts 6  
user: james  
user: ../../../../../../../../etc/bash_completion.d  
user: thomas  
user: john  
user: mindy  
user: mailadmin
```

You can see our arbitrary-write-user is now here :^) but again, someone has to log into the machine and no one is actually using the box  so this won't work.

I can also change all the account passwords (this is generally not good practice)
![[Pasted image 20230408024208.png]]

## Potential Email Addresses
```
webadmin@solid-state-security.com [CONFIRMED]
mailadmin@solid-state-security.com
thomas@solid-state-security.com
john@solid-state-security.com
mindy@solid-state-security.com
james@solid-state-security.com
```

I will now log in to each account [not really].

I have successful login. Now it's time for guessy bullshit and try to find which user has sensitive emails [if any emails what-so-ever]. This is the boring part [so I just lookup who has the secret sauce :^)]... suprise, it's John...

![[Pasted image 20230408031624.png]]
John has 1 email.

![[Pasted image 20230408031707.png]]
```
Return-Path: <mailadmin@localhost>  
Message-ID: <9564574.1.1503422198108.JavaMail.root@solidstate>  
MIME-Version: 1.0  
Content-Type: text/plain; charset=us-ascii  
Content-Transfer-Encoding: 7bit  
Delivered-To: john@localhost  
Received: from 192.168.11.142 ([192.168.11.142])  
         by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 581  
         for <john@localhost>;  
         Tue, 22 Aug 2017 13:16:20 -0400 (EDT)  
Date: Tue, 22 Aug 2017 13:16:20 -0400 (EDT)  
From: mailadmin@localhost  
Subject: New Hires access  
John,    
  
Can you please restrict mindy's access until she gets read on to the program. Also make sure that you send her a tempory password to login to her accounts.  
  
Thank you in advance.  
  
Respectfully,  
James
```

This indicating that a temporary password is likely still valid, but unsure. I can check Mindy's email to see if there's any more information.

#### Email 1
```
Return-Path: <mailadmin@localhost>  
Message-ID: <5420213.0.1503422039826.JavaMail.root@solidstate>  
MIME-Version: 1.0  
Content-Type: text/plain; charset=us-ascii  
Content-Transfer-Encoding: 7bit  
Delivered-To: mindy@localhost  
Received: from 192.168.11.142 ([192.168.11.142])  
         by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 798  
         for <mindy@localhost>;  
         Tue, 22 Aug 2017 13:13:42 -0400 (EDT)  
Date: Tue, 22 Aug 2017 13:13:42 -0400 (EDT)  
From: mailadmin@localhost  
Subject: Welcome  
  
Dear Mindy,  
Welcome to Solid State Security Cyber team! We are delighted you are joining us as a junior defense analyst. Your role is critical in fulfilling the mission of our orginzation. The enclosed information is designe  
d to serve as an introduction to Cyber Security and provide resources that will help you make a smooth transition into your new role. The Cyber team is here to support your transition so, please know that you can  
call on any of us to assist you.  
  
We are looking forward to you joining our team and your success at Solid State Security.    
  
Respectfully,  
James
```

#### Email 2
```
Return-Path: <mailadmin@localhost>  
Message-ID: <16744123.2.1503422270399.JavaMail.root@solidstate>  
MIME-Version: 1.0  
Content-Type: text/plain; charset=us-ascii  
Content-Transfer-Encoding: 7bit  
Delivered-To: mindy@localhost  
Received: from 192.168.11.142 ([192.168.11.142])  
         by solidstate (JAMES SMTP Server 2.3.2) with SMTP ID 581  
         for <mindy@localhost>;  
         Tue, 22 Aug 2017 13:17:28 -0400 (EDT)  
Date: Tue, 22 Aug 2017 13:17:28 -0400 (EDT)  
From: mailadmin@localhost  
Subject: Your Access  
  
Dear Mindy,  
  
  
Here are your ssh credentials to access the system. Remember to reset your password after your first login.    
Your access is restricted at the moment, feel free to ask your supervisor to add any commands you need to your path.    
  
username: mindy  
pass: P@55W0rd1!2@  
  
Respectfully,  
James
```

Logging into SSH with Mindy gives some really fucky output, likely from the earlier Apache James exploit that didn't work. Now I am logged in:
![[Pasted image 20230408032545.png]]



