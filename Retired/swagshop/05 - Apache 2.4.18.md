![[Pasted image 20230504215726.png]]
Appears as though it wants to resolve hostname.

![[Pasted image 20230504223034.png]]
![[Pasted image 20230504223107.png]]
## Search request
![[Pasted image 20230504223253.png]]
Search paramter does not appear to be vulnerable to SQLi

## account creation
![[Pasted image 20230504224007.png]]
#### Request
![[Pasted image 20230504224130.png]]
#### Response
![[Pasted image 20230504224301.png]]
![[Pasted image 20230504224330.png]]
![[Pasted image 20230504224357.png]]
```
From your My Account Dashboard you have the ability to view a snapshot of your recent account activity and update your account information. Select a link below to view or edit information.
```

The form does seem to accept XML.

## product purchase

![[Pasted image 20230504224924.png]]
## directories
```
┌──(lemur㉿kali)-[~/htb/swagshop]  
└─$ gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt -u http://swagshop.htb -n -x php -o logs/feroxbuster.log -t 50  
===============================================================  
Gobuster v3.5  
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)  
===============================================================  
[+] Url:                     http://swagshop.htb  
[+] Method:                  GET  
[+] Threads:                 50  
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt  
[+] Negative Status codes:   404  
[+] User Agent:              gobuster/3.5  
[+] Extensions:              php  
[+] No status:               true  
[+] Timeout:                 10s  
===============================================================  
2023/05/04 23:26:25 Starting gobuster in directory enumeration mode  
===============================================================  
/.php                 [Size: 291]  
/index.php            [Size: 16593]  
/media                [Size: 312] [--> http://swagshop.htb/media/]  
/includes             [Size: 315] [--> http://swagshop.htb/includes/]  
/install.php          [Size: 44]  
/lib                  [Size: 310] [--> http://swagshop.htb/lib/]  
/app                  [Size: 310] [--> http://swagshop.htb/app/]  
/js                   [Size: 309] [--> http://swagshop.htb/js/]  
/api.php              [Size: 37]  
/shell                [Size: 312] [--> http://swagshop.htb/shell/]  
/skin                 [Size: 311] [--> http://swagshop.htb/skin/]  
/cron.php             [Size: 0]  
/var                  [Size: 310] [--> http://swagshop.htb/var/]  
/errors               [Size: 313] [--> http://swagshop.htb/errors/]  
/mage                 [Size: 1319]  
/.php                 [Size: 291]  
Progress: 175031 / 175330 (99.83%)  
===============================================================  
2023/05/04 23:29:15 Finished  
===============================================================
```

![[Pasted image 20230504233429.png]]
![[Pasted image 20230504233513.png]]
```bash
#!/bin/sh

# REPLACE with your PHP5 binary path (example: /usr/local/php5/bin/php )
#MAGE_PHP_BIN="php"

MAGE_PHP_SCRIPT="mage.php"
DOWNLOADER_PATH='downloader'

# initial setup
if test "x$1" = "xmage-setup"; then
    echo 'Running initial setup...'

    if test "x$2" != "x"; then
        MAGE_ROOT_DIR="$2"
    else
        MAGE_ROOT_DIR="`pwd`"
    fi

    $0 config-set magento_root "$MAGE_ROOT_DIR"
    $0 config-set preferred_state beta
    $0 channel-add http://connect20.magentocommerce.com/community
    exit
fi

# check that mage pear was initialized

if test "x$1" != "xconfig-set" &&
  test "x$1" != "xconfig-get" &&
  test "x$1" != "xconfig-show" &&
  test "x$1" != "xchannel-add" &&
  test "x`$0 config-get magento_root`" = "x"; then
    echo 'Please initialize Magento Connect installer by running:'
    echo "$0 mage-setup"
    exit;
fi

# find which PHP binary to use
if test "x$MAGE_PHP_BIN" != "x"; then
  PHP="$MAGE_PHP_BIN"
else
  PHP=php
fi


# get default pear dir of not set
if test "x$MAGE_ROOT_DIR" = "x"; then
    MAGE_ROOT_DIR="`pwd`/$DOWNLOADER_PATH"
fi

exec $PHP -C -q $INCARG -d output_buffering=1 -d variables_order=EGPCS \
    -d open_basedir="" -d safe_mode=0 -d register_argc_argv="On" \
    -d auto_prepend_file="" -d auto_append_file="" \
    $MAGE_ROOT_DIR/$MAGE_PHP_SCRIPT "$@"
```

```
Magento SMTP Pro Extension by Ashley Schroder (aschroder.com)

-   Free and Opensource email extension for Magento
-   Easily send Magento transactional emails via Google Apps, Gmail, Amazon SES or your own SMTP server.

-   Test your conifguration from the Magento admin
-   View a log of all emails
-   Improve deliverability with an external SMTP server
```

- https://github.com/protechhelp/gamamba/blob/master/mage

Alot of these directories listed in the scan are part of this mage(ento) script. However, what's not obvious at first glance is this:
![[Pasted image 20230504235703.png]]
![[Pasted image 20230504235936.png]]

