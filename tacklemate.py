#!/usr/bin/env python
import os
import subprocess
import flask
import tensorflow_hub as hub
import formula

app = flask.Flask(__name__, template_folder='static/templates')
username = "fake_username"
given = "Name"
model =  None


def load_model():
    global model
    try:
        model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
        model = model.signatures['serving_default'] # default model
        load_status = True
    except Exception as e:
        model = None
        load_status = False

    return load_status

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    if model is None:
        load_status = load_model()
    else:
        load_status = True # model already loaded

    html_code = flask.render_template('index.html', username=username,
                                    given=given, load_status=load_status)
    response = flask.make_response(html_code)

    return response



@app.route('/upload_video', methods=['POST'])
def upload_video():

    print("\n")
    print("-----------------------------------------------------------")
    print("Received upload request in python server")

    # In case user deletes tacklemate-videos dir
    path = "./tacklemate-videos"
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)


    f = flask.request.files['video_file']
    f.save(f"./tacklemate-videos/{f.filename}")

    print("Successfully saved file", f.filename)
    print("-----------------------------------------------------------")
    #formula(f.filename)
    resp = {"success": True, "response": "file saved!", "filename": f.filename}
    return flask.jsonify(resp), 200



@app.route('/get_scores', methods=['GET', 'POST'])
def get_scores():

    video_fn = flask.request.args.get("fn")
    timestamp = float(flask.request.args.get("timestamp"))
    side = flask.request.args.get("side")

    # Calculate the tackle score
    video_path = f"./tacklemate-videos/{video_fn}"
    scores, length = formula.score(model, video_path, timestamp, side)
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

    arm_score = scores["arm"]
    arm_rating = rating[arm_score]

    html_code = flask.render_template('results.html', username=username,
            given=given, video_fn=video_fn, timestamp=round(timestamp, 2),
            height_score=height_score, height_rating=height_rating,
            height_feedback=height_feedback, arm_score=arm_score,
            arm_rating=arm_rating, length=length)
    response = flask.make_response(html_code)
    return response



@app.route('/stats', methods=['GET'])
def stats():

    html_code = flask.render_template('stats.html', username=username,
                                        given=given)
    response = flask.make_response(html_code)
    return response



@app.errorhandler(404)
def page_not_found(e):

    html_code = flask.render_template('404.html', username=username,
                                        given=given)
    response = flask.make_response(html_code)
    return response



if __name__ == '__main__':
    #os.system("gunicorn tacklemate:app")
    app.run(debug=True, port=50001, ssl_context='adhoc')