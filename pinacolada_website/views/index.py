from flask import current_app, Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
import re
from ansi2html import Ansi2HTMLConverter

conv = Ansi2HTMLConverter()
ansi_escape = re.compile(r'\x1b[^m]*m')
mod = Blueprint('index', __name__)
cli_init = False
CLI_INIT = 10
CLI = 11
CLI_RESP = 12

@mod.route('/')
def index():
    s = current_app.config["server"]
    print " + Sending command to pi..."
    s.send_to_pi(CLI_INIT, "0", "cli init")
    s.pi_resp_event.wait()
    s.pi_resp_event.clear()
    resp = ansi_escape.sub('', "\n".join(s.pi_resp.rstrip().split("\n")[:-1]))  # strip prompt and ansi
    return render_template('index/index.html', greetings=resp)

'''
@mod.route('/terminal/')
def terminal():
    s = current_app.config["server"]
    print " + Sending command to pi..."
    s.send_to_pi(CLI_INIT, "0", "cli init")
    s.pi_resp_event.wait()
    s.pi_resp_event.clear()
    #resp = ansi_escape.sub('', s.pi_resp)
    prompt = s.pi_resp.split("\n")[-1]
    print "I THINK THE PROMPT IS %s " % prompt
    resp = conv.convert("\n".join(s.pi_resp.rstrip().split("\n")[:-1]))
    return render_template('index/terminal.html', greetings=resp)
'''

@mod.route('/command/', methods=['POST'])
def post():
    data = {}
    command = request.form['command']
    s = current_app.config["server"]
    s.send_to_pi(CLI, "0", command)
    s.pi_resp_event.wait()
    s.pi_resp_event.clear()

    data["prompt"] = ansi_escape.sub('', (s.pi_resp.split("\n")[-1]))
    data["response"] = conv.convert("\n".join(s.pi_resp.rstrip().split("\n")[:-1]))
    return jsonify(**data)
