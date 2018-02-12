# Introduction

Lithophone is a simple web server intended to store and return messages.

It uses SQLite internally, and isn't implemented with serious performance in
mind. If bottlenecked, a more performant SQL server would help.

# Usage

The developer tested this server with the Gunicorn server, and by adding more
workers, it can scale relatively well with that system. However, any
WSGI-compliant server should do the trick.

