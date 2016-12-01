from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
import json

# class Index():
# 	def __init__(self, server):
# 		self.server = server
# 		self.mod = Blueprint('index', __name__)

# 		@self.mod.route('/')
# 		def index():
# 		    return render_template(
# 		        'index/index.html'
# 		    )

# 		@self.mod.route('/terminal/')
# 		def terminal():
# 		    return render_template(
# 		        'index/terminal.html'
# 		    )
# 		@self.mod.route('/command/', methods=['POST'])
# 		def post():
# 			command = request.form['command']
# 			print command

mod = Blueprint('index', __name__)

@mod.route('/')
def index():
    return render_template(
        'index/index.html'
    )

@mod.route('/terminal/')
def terminal():
    return render_template(
        'index/terminal.html'
    )
@mod.route('/command/', methods=['POST'])
def post():
	return "YOU TYPED: " + request.form['command']
