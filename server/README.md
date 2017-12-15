# Server-side Implementation of CS523 IoT UI Project

Our server is implemented on top of following components. Please consider following components when setting up the server. We tested and verfied all components on Ubuntu 16.04 which is hosted by a micro-instance of Amazon EC2.

## Prerequisites

* [Python (Flask)] - We used Flask as our main platfrom for server code. In addition, we leveraged PyCrypto for encryption/decryption operations.
* [MySQL] - Backend database
* [Apache] - Not necessary, but essential for stable server setup

To simply run our server side code without Apache setup, use command

```
python iot_server.py
```