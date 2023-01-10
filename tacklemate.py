#!/usr/bin/env python
import os
import flask
import logging
from google.cloud import storage
import formula

app = flask.Flask(__name__, template_folder='static/templates')
app.secret_key = os.environ['APP_SECRET_KEY']

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
#----------------------------------------------------------------------

# Routes for authentication

@app.route('/login', methods=['GET'])
def login():
    return auth.login()

@app.route('/login/callback', methods=['GET'])
def callback():
    return auth.callback()

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return auth.logoutapp()

@app.route('/logoutgoogle', methods=['GET'])
def logoutgoogle():
    return auth.logoutgoogle()

#----------------------------------------------------------------------


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    app.logger.info("entering index function")
    username = auth.authenticate()
    given = flask.session.get('given_name')

    html_code = flask.render_template('index.html', username=username,
                                    given=given)
    response = flask.make_response(html_code)

    return response

@app.route('/upload_video', methods=['POST'])
def upload_video():

    print("Received video upload request")
    tackle_vid = flask.request.files['video_file']

    # ID of Google Cloud Storage bucket
    bucket_name = os.environ['TACKLE_BUCKET_NAME']

    # Name of the uploaded GCS object
    # TODO: replace this with int key using sql query to all the videos?
    destination_blob_name = "test_upload_video.mp4"

    # Construct a client-side representation of the blob.
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Rewind the stream to the beginning. This step can be omitted if the input
    # stream will always be at a correct position.
    tackle_vid.seek(0)

    # Upload data from the stream to your bucket.
    blob.upload_from_file(tackle_vid, content_type="video/mp4")

    print(
        f"Tackle video successfully uploaded as {destination_blob_name} \
        to the {bucket_name} bucket in TackleMate's Google Cloud Storage"
    )
    resp = {"success": True, "response": "file uploaded!", "filename": tackle_vid.filename}
    return flask.jsonify(resp), 200


@app.route('/get_scores', methods=['GET', 'POST'])
def get_scores():

    # somewhere in this function is where the error occurs...
    username = auth.authenticate()
    given = flask.session.get('given_name')

    video_fn = flask.request.args.get("fn")
    timestamp = float(flask.request.args.get("timestamp"))
    print("Video filename", video_fn)
    print("Tackle timestamp:", timestamp)


     # Calculate the tackle score
     # THIS LINE CAUSES SERVER ERROR
    scores, length = formula.score(video_fn, timestamp)


    rating = {0:"poor", 1:"fair", 2:"good", 3:"excellent"}
    h_feeback = \
        {0:"Minimal change in height at tackle. Try to bend the knees \
            and drop the shoulders.",
        1:"Some decrease in height at tackle. Try to drop to where the \
            ball carrier's knees would be.", \
        2:"Good decrease in height at tackle! Try to drop to where the \
            ball carrier's knees would be.",
        3:"Excellent drop in height! As an excercise, try to brush the \
            hands against the ground before making contact."}

    height_score = scores["height"]
    height_rating = rating[height_score]
    height_feedback = h_feeback[height_score]

    html_code = flask.render_template('results.html', username=username,
            given=given, video_fn=video_fn, timestamp=round(timestamp, 2),
            height_score=height_score, height_rating=height_rating,
            height_feedback=height_feedback, length=length)
    response = flask.make_response(html_code)
    return response



@app.route('/stats', methods=['GET'])
def stats():

    username = auth.authenticate()
    given = flask.session.get('given_name')
    html_code = flask.render_template('stats.html', username=username,
                                        given=given)
    response = flask.make_response(html_code)
    return response

@app.errorhandler(404)
def page_not_found(e):
    username = auth.authenticate()
    given = flask.session.get('given_name')
    html_code = flask.render_template('404.html', username=username,
                                        given=given)
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
