# Introduction

Lithophone is a simple web server intended to store and return messages.

It uses SQLite internally, and isn't implemented with serious performance in
mind. If bottlenecked, a more performant SQL server would help.

# Usage

This is packaged with a Docker environment. If you have docker and docker-compose
installed  it should be as easy as running

    docker-compose build
    docker-compose up -d

After this you will find the service listening on http://localhost:8080

To clean up run

    docker-compose down

To run manually outside of Docker using gunicorn (where 4 can be changed to
the desired number of workers).

    cd src
    gunicorn -w 4 lithophone:app


It can scale relatively well with gunicorn system. However, any
WSGI-compliant server should do the trick.

# Notes

By default the post cache file will be stored at `/tmp/lithophone.db` unless
overidden by the `CACHE_FILE` environmental variable. This file is a sqlite DB if you are curious.

