#!/usr/bin/env python3.6
import sqlite3
import json


db = sqlite3.connect(':memory:', check_same_thread=False)
db.execute("""CREATE TABLE IF NOT EXISTS webhook_messages (
                target, message)""")
db.commit()


def app(env, start_response):
    target = env['PATH_INFO'][1:]
    if not target:
        start_response('404 NOT FOUND', [])
        return []

    cursor = db.cursor()

    if env['REQUEST_METHOD'] == 'POST':
        cursor = db.cursor()

        cursor.execute(
            'INSERT INTO webhook_messages VALUES (?, ?)', (target,
                env['wsgi.input'].read()))

        db.commit()
        cursor.close()

        start_response('200 OK', [])
        return []


    elif env['REQUEST_METHOD'] == 'GET':
        received = cursor.execute("""
            SELECT rowid, message FROM
            webhook_messages WHERE
            target = '{}'""".format( target)).fetchall()


        messages = []
        message_ids = []
        for message_id, message in received:
            message_ids.append(str(message_id))
            try:
                messages.append(json.loads(message))
            except ValueError:
                messages.append(message)

        cursor.execute(
            "DELETE FROM webhook_messages WHERE rowid IN ({})".format(
                ','.join(message_ids)))

        db.commit()
        cursor.close()

        start_response('200 OK', [
            ( 'Content-Type', 'application/json')])
        return [bytes(json.dumps([str(m) for m in messages]), 'utf-8')]
    else:
        start_response('400 BAD REQUEST', [])
        return []
