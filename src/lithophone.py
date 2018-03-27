#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json
import logging
import sqlite3
from array import array

from functools import lru_cache


@lru_cache(maxsize=1)
def get_logger():
    logger = logging.getLogger(__name__)
    return logger


@lru_cache(maxsize=1)
def get_db_connection(db_file):
    db = sqlite3.connect(db_file, check_same_thread=False)
    db.execute("""CREATE TABLE IF NOT EXISTS webhook_messages (
                    target, message, content_type)""")
    db.commit()
    return db


def app(env, start_response):
    logger = get_logger()

    target = env['PATH_INFO'][1:]
    if not target:
        start_response('404 NOT FOUND', [])
        return []

    # This is cached so it only actually runs once even if the script is long lived.
    db_file = env.get('CACHE_FILE', "/tmp/lithophone.db")
    db = get_db_connection(db_file)

    cursor = db.cursor()

    if env['REQUEST_METHOD'] == 'POST':
        logging.info("Got post for '{}'".format(target))
        message = env['wsgi.input'].read()
        cursor.execute(
            'INSERT INTO webhook_messages VALUES (?, ?, ?)', (target,
                                                              message, None))

        db.commit()
        cursor.close()

        start_response('200 OK',
                       [('Content-Type', 'text/plain')])
        return []

    elif env['REQUEST_METHOD'] == 'GET':
        received = cursor.execute("""
            SELECT rowid, message FROM
            webhook_messages WHERE
            target = '{}'""".format(target)).fetchall()

        messages = []
        message_ids = []
        for message_id, message in received:
            message_ids.append(str(message_id))
            messages.append(message.decode('utf-8'))

        cursor.execute(
            "DELETE FROM webhook_messages WHERE rowid IN ({})".format(
                ','.join(message_ids)))

        db.commit()
        cursor.close()

        if len(messages) == 0:
            start_response('204 NO CONTENT', [
                ('Content-Type', 'text/plain')])
            return []

        response = [bytes(json.dumps(messages), 'utf-8')]
        logger.info("Target '{}' has {} messages: {}".format(target,
                                                             len(messages), response))

        start_response('200 OK', [
            ('Content-Type', 'application/json')])

        return response

    else:
        start_response('400 BAD REQUEST', [])
        return []
