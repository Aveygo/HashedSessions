# HashedSessions
[![Aveygo - HashedSessions](https://img.shields.io/static/v1?label=Aveygo&message=HashedSessions&color=black&logo=github)](https://github.com/Aveygo/HashedSessions "Go to GitHub repo")
[![stars - HashedSessions](https://img.shields.io/github/stars/Aveygo/HashedSessions?style=social)](https://github.com/Aveygo/HashedSessions)   [![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT) [![Python 3.9.9](https://img.shields.io/badge/python-3.9.9-black.svg)](https://www.python.org/downloads/release/python-399/)

Create sessions with hashing, pure-python.

## How it works

Normally a session is signed cryptographically but this method may be slow and results in long signatures eg: ecdsa = 64 bytes.

However by taking the user's data, appending a secret, and hashing, we can generate a pseudo signature where only the owners of the secret can calculate said hash.
By appending this hash to the original data, we create a usable session token.

```
session = user_data + hash(user_data + timestamp + secret)
```

See the SessionManager class in main.py to see an example.

Note, this is more of a proof of concept, please don't use in production.
