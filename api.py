from flask import Flask, request, render_template, send_file
from flask_restful import Resource, Api
from openai import OpenAI
import os


app = Flask(__name__)
api = Api(app)

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key = "sk-no-key-required"
)


###
# Define endpoint actions.
###

class ProcessMessage(Resource):
    def get(self):
        req = request.args.get('t')

        completion = client.chat.completions.create(
            model="LLaMA_CPP",
            messages=[
                {"role": "system", "content": "You will be given an SMS message and you will provide a funny response."},
                {"role": "user", "content": req}
            ]
        )

        return completion.choices[0].message.content


class ProcessImage(Resource):
    def get(self):
        req = request.args.get('t')
        req = "Make a funny meme in response to this SMS message: {0}".format(req)

        cmd = """ docker run --rm -it -v /home/nick/working/texty:/data sd2 bash -c "cd / && python3 sd2.py '{0}' " """.format(req)
        os.system(cmd)

        return "OK"


@app.route('/get_img')
def get_image():
    return send_file("meme.png", mimetype='image/png')


@app.route('/get_img_html')
def get_image_html():
    return send_file("meme.html", mimetype='text/html')


###
# Attach endpoints.
###

api.add_resource(ProcessMessage, '/msg')
api.add_resource(ProcessImage, '/img')


###
# Start server.
###

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
