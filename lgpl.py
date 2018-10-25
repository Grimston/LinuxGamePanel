#!/usr/bin/env python3
"""
pip requirements
flask ansi2html pam
"""
import sys
from json import dumps, loads
from os import path
from random import SystemRandom
from shlex import split
from string import ascii_lowercase, punctuation, ascii_uppercase, digits
from subprocess import Popen, PIPE

import pam
from ansi2html import Ansi2HTMLConverter
from flask import Flask, session, redirect, url_for, request, render_template, flash
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

# Default config - Set in lgpl.json
config = dict(servers=['lgsm-script-here'], use_pam=True, admin_username='admin', admin_password='admin',
              host='0.0.0.0', port=8000, secret_key=''.join(
        SystemRandom().choice(
            ascii_lowercase + ascii_uppercase + digits + punctuation)
        for _ in range(21)))


def save_config():
    with open('lgpl.json', 'w') as config_file:
        config_file.write(dumps(config, sort_keys=True, indent=4))


def load_config():
    global config
    if path.isfile("lgpl.json"):
        with open('lgpl.json', 'r') as config_file:
            config = loads(config_file.read())
    else:
        save_config()  # Saves the default config to the disk for the user to edit

    app.secret_key = config["secret_key"].encode()


@app.route('/api/restart/<server>')
def api_restart(server):
    if 'username' in session:
        exitcode, out, err = get_exitcode_stdout_stderr("./" + server + " restart")
        conv = Ansi2HTMLConverter(inline=True)
        return conv.convert(out.decode('utf-8'))


@app.route('/api/start/<server>')
def api_start(server):
    if 'username' in session:
        exitcode, out, err = get_exitcode_stdout_stderr("./" + server + " start")
        conv = Ansi2HTMLConverter(inline=True)
        return conv.convert(out.decode('utf-8'))


@app.route('/api/stop/<server>')
def api_stop(server):
    if 'username' in session:
        exitcode, out, err = get_exitcode_stdout_stderr("./" + server + " stop")
        conv = Ansi2HTMLConverter(inline=True)
        return conv.convert(out.decode('utf-8'))


@app.route('/api/update/<server>')
def api_update(server):
    if 'username' in session:
        exitcode, out, err = get_exitcode_stdout_stderr("./" + server + " update")
        conv = Ansi2HTMLConverter(inline=True)
        return conv.convert(out.decode('utf-8'))


@app.route('/api/validate/<server>')
def api_validate(server):
    if 'username' in session:
        exitcode, out, err = get_exitcode_stdout_stderr("./" + server + " validate")
        conv = Ansi2HTMLConverter(inline=True)
        return conv.convert(out.decode('utf-8'))


@app.route('/api/details/<server>')
def api_details(server):
    if 'username' in session:
        exitcode, out, err = get_exitcode_stdout_stderr("./" + server + " details")
        conv = Ansi2HTMLConverter(inline=True)
        return conv.convert(out.decode('utf-8'))


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('server_list'))

    return render_template('index.html')


@app.route('/control/<server>')
def control(server):
    if 'username' not in session:
        flash("You do not have access to this section, please login!")
        return redirect(url_for('index'))

    return render_template('control.html', username=session['username'], servers=config['servers'], server=server)


@app.route('/selection')
def server_list():
    if 'username' not in session:
        flash("You do not have access to this section, please login!")
        return redirect(url_for('index'))

    return render_template('server_list.html', username=session['username'], servers=config['servers'])


@app.route('/login', methods=['POST'])
def login():
    if config['use_pam']:
        p = pam.pam()
        if p.authenticate(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('server_list'))
    else:
        if request.form['username'] == config['admin_username'] and request.form['password'] == config['admin_password']:
            session['username'] = request.form['username']
            return redirect(url_for('server_list'))

    flash("Username/Password was invalid!")
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = split(cmd)

    process = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    exitcode = process.returncode

    return exitcode, out, err


if __name__ == "__main__":
    sys.stdout = open('log/web/lgpl.log', 'w')
    load_config()
    WSGIRequestHandler.protocol_version = "HTTP/1.1"  # Enables keep-alive support so long scripts will finish
    app.run(host=config['host'], port=config['port'])
