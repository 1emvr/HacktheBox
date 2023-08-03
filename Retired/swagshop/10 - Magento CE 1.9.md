```
IV. DESCRIPTION  
-------------------------  
  
The aforementioned XXE vulnerability in Zend Framework which affects eBay  
Magento, was assigned a CVE-ID of CVE-2015-5161 and can be found in a  
separate advisory at:  
  
http://legalhackers.com/advisories/zend-framework-XXE-vuln.txt  
  
In short, the Zend Framework XXE vulnerability stems from an insufficient  
sanitisation of untrusted XML data on systems that use PHP-FPM to serve PHP  
applications.  
By using certain multibyte encodings within XML, it is possible to bypass  
the sanitisation and perform certain XXE attacks.  
  
Since eBay Magento is based on Zend Framework and uses several of its XML  
classes, it also inherits this XXE vulnerability.  
  
The vulnerability in Zend affects all its XML components, however there  
are two vulnerable Zend Framework vulnerable components:  
  
- Zend_XmlRpc_Server  
- Zend_SOAP_Server
```

![[Pasted image 20230505000532.png]]

```
...
Magento implements a store API providing XML/SOAP web services.  
Although the Zend_XmlRpc is present within Magento code base, the testing  
revealed that an older Zend class was used for its implementation, which is  
not vulnerable.  
  
However, further testing revealed that Magento SOAP API was implemented using  
the Zend_SOAP_Server class from Zend Framework, which is vulnerable to the  
XXE injection vulnerability discovered earlier.
```

![[Pasted image 20230505001050.png]]
`http://swagshop.htb/index.php/api/soap`

## Proof of concept script
![[Pasted image 20230505001318.png]]
![[Pasted image 20230505001543.png]]

*"SOAP extension is not loaded"* means what it says. I should have known that from visiting in browser but I wanted to try it anyway.

## Magento RCE
```
**What kind of attack is it?**

The vulnerability is actually comprised of a chain of several vulnerabilities that ultimately allow an unauthenticated attacker to execute PHP code on the web server. The attacker bypasses all security mechanisms and gains control of the store and its complete database, allowing credit card theft or any other administrative access into the system.

This attack is not limited to any particular plugin or theme. All the vulnerabilities are present in the Magento core, and affects any default installation of both Community and Enterprise Editions. Check Point customers are already protected from exploitation attempts of this vulnerability through the IPS software blade.
```

I'm not 100% sure of the version this Magento is but i'm going to give it a shot, anyway. It's an SQLi vulnerability using default credentials.
https://github.com/joren485/Magento-Shoplift-SQLI

![[Pasted image 20230505002652.png]]

`ypwq:123`
