"""
Simple Flask web site 
"""

import flask    # The basic framework for http requests, storing cookies, etc
import flask_sslify

import logging  # For monitoring and debugging
import os

###
# Globals
###

import CONFIG   # Separate out per-machine configuration 
app = flask.Flask(__name__)   
app.secret_key = CONFIG.COOKIE_KEY
app.logger.setLevel(logging.DEBUG)
# On Heroku, debugging must be off to run https
if 'DYNO' in os.environ: 
    app.debug=False
    sslify = flask_sslify.SSLify(app)
else:
    app.debug=CONFIG.DEBUG


#################
# Pages and request handling:
# We "route" URLs to functions by attaching
# the app.route 'decorator'.
#
# I typically use the same base name for URL, function,
# and html template, but that is just for readability ---
# url "/foo" could call function "bar()" which could
# render page "zot.html". 
#
#################

@app.route("/")
@app.route("/index")
def index():
  return flask.render_template('index.html')

@app.route("/form")
def form():
    return flask.render_template('form.html')

#################
# Handle a form, then redirect back to the
# index page
#################
@app.route("/_submit", methods=['POST'])
def ranted():
  app.logger.debug("Submitted: |{}|".format(flask.request.form))
  rant = flask.request.form["rant"]
  flask.session["rant"] = rant
  return flask.redirect(flask.url_for('index'))

###################
#   Error handlers
#   These are pages we display when something goes wrong
###################
@app.errorhandler(404)
def error_404(e):
  app.logger.warning("++ 404 error: {}".format(e))
  return flask.render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
  app.logger.warning("++ 500 error: {}".format(e))
  assert app.debug == False  ## Crash me please, so I can debug! 
  return flask.render_template('500.html'), 500

@app.errorhandler(403)
def error_403(e):
  app.logger.warning("++ 403 error: {}".format(e))
  return flask.render_template('403.html'), 403


###############
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#   (Currently none, leaving this here as an example)
###############
# @app.route("/_check")
# def _check():
#   tray = request.args.get("tray", "", type=str)
#   pattern = request.args.get("pattern", "XXX", type=str)
#   matches = find.search(WORDS, pattern, tray)
#   ### Matches returns a list of words
#   return jsonify(result={ "words": " ".join(matches) })

#############
# Filters
# These process some text before inserting into a page
#############
@app.template_filter('humanize')
def humanize(date):
    """Humanize an ISO date string"""
    as_arrow = arrow.get(date)
    return as_arrow.humanize()

# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#
if __name__ == "__main__":
    # Running standalone
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server, 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service. 
    pass


