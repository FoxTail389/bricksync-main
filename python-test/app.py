from gradio_client import Client, file
from flask import Flask, jsonify
app = Flask(__name__)
def test():
    client = Client("FoxTail389/BrickSync")
    result = client.predict(
            image=file('https://raw.githubusercontent.com/FoxTail389/bricksync/86197932b87c192575fba47c184694e7453227dc/api/News%20Recording.png'),
            audio=file('https://github.com/FoxTail389/bricksync/raw/86197932b87c192575fba47c184694e7453227dc/api/News%20Recording.wav'),
            gender="Male",
            leftpixel=120,
            Json=[[827,596],[939,596],[883,585]],
            api_name="/predict"
    )
    print(result)
    return jsonify(result)
@app.route("/")
def hello_world():
    return test()
if __name__ == "__main__":
    app.run()