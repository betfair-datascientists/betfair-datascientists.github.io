# Creating Betfair API Certificates with OpenSSL on Windows

This guide walks through generating Betfair API certificates from scratch using OpenSSL on Windows.

## Why use certificates?

The certificate proves:

 - The request is coming from a **trusted registered client**
 - The client owns the private key associated with the uploaded certificate

When you upload a certificate to Betfair:

 - Betfair stores the public certificate
 - You keep the private key locally
 - Requests signed using that key can be validated by Betfair

If someone steals:

 - your username/password → still not enough
 - your app key → still not enough
 - they ALSO need your private key → otherwise authentication fails

Think of authentication like this:

| Component | Role |
|----------|------|
| Username/password | Who you are |
| App key | Which application you are using |
| Certificate | Proof your application is trusted |

The certificate is the **strongest binding factor** between your code and your account.

---

## 1. Install OpenSSL

[Download the Windows installer](https://slproweb.com/products/Win32OpenSSL.html)

Install:

 - Win64 OpenSSL if using 64-bit Windows
 - Use default installation settings

During installation select **"Copy OpenSSL DLLs to: The OpenSSL binaries (/bin) directory"**

---

## 2. Create a working directory for creating certificates

e.g. "C:\Users\Mitch\Documents\Betfair_Certs"

---

## 3. Open OpenSSL Installation

 - Open **Win64 OpenSSL Command Prompt** from the Windows Search Bar
 - Change the working directory using the command "cd" - e.g. "cd C:\Users\Mitch\Documents\Betfair_Certs"

---

## 4. Generate Private Key

Run:

```OpenSSL
openssl genrsa -out client-2048.key 2048
```

This creates:

```text
client-2048.key
```

This is your private certificate key.

---

## 5. Generate Certificate Signing Request (CSR)

Run:

```OpenSSL
openssl req -new -key client-2048.key -out client-2048.csr
```

You will be prompted for certificate information.

Example:

```text
Country Name (2 letter code) [AU]:AU
State or Province Name (full name) []:Victoria
Locality Name (eg, city) []:Melbourne
Organization Name (eg, company) []:Personal
Organizational Unit Name (eg, section) []:API
Common Name (e.g. server FQDN or YOUR name) []:Betfair API
Email Address []:your@email.com
```

For these fields simply press Enter:

```text
A challenge password []:
An optional company name []:
```

This creates:

```text
client-2048.csr
```

For anything regarding organization, simply enter '.' and it will be blank

---

## 6. Generate Self-Signed Certificate

Run:

```OpenSSL
openssl x509 -req -days 365 -in client-2048.csr -signkey client-2048.key -out client-2048.crt
```

This creates:

```text
client-2048.crt
```

You should now have:

```text
client-2048.key
client-2048.csr
client-2048.crt
```

The `.csr` file is no longer needed after the certificate is created.

---

## 7. Create the .pem file

In any text-editor, combine the text from the client-2048.key and client-2048.crt files into a new file.
Save this file as 'client-2048.pem'

After saving, check that the file is client-2048.pem and **NOT** client-2048.pem.txt

---

## 8. Upload Certificate to Betfair

Login to Betfair.

Navigate to https://myaccount.betfair.com.au/accountdetails/mysecurity?showAPI=1

Upload the below file to **Automated Betting Program Access**

```text
client-2048.crt
```

Do **NOT** upload the `.key` file.

---

## 9. Using Certificates in Python (betfairlightweight)

Example:

```python

from betfairlightweight import APIClient
import pprint

certs_path = 'C:\Users\Mitch\Documents\Betfair_Certs'

trading = APIClient(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD',
    app_key='YOUR_APP_KEY',
    certs=certs_path
)

login_response = trading.login()
pprint.pprint(vars(login_response))

```

Folder structure example:

```text
C:\Users\Mitch\Documents\Betfair_Certs\
    client-2048.pem
```

---

## 10. Notes

- Betfair Australia users do NOT require a separate developer account
- Certificates are required for non-interactive login
- Keep your `.key` file private
- Never share the private key publicly

---

## Further Support

Australian customers can email us for support at automation@betfair.com.au