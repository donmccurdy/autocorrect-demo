#Simple AutoCorrect Demo#

Note: The dictionary used is the unabridged text of Moby Dick, so many modern words will not be recognized. Contractions are also not corrected.

DEMO: *Currently Unavailable*

----

To run this project, you'll need to do two things:

1) Open assets/py/spellchecker.py, and around line 17 find there is a line that reads:

> _server = SimpleXMLRPCServer(('206.217.131.124', 9000), logRequests=True)_

   You'll need to change the IP address and/or port to match your server. Running locally, 'localhost' will do.

2) Make sure you have permissions to execute, and call 'nohup | ./spellchecker.py &' to start the XML-RPC server as a daemon.

----

Don McCurdy, 2012.
