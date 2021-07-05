from flask import Flask, render_template, url_for
from threading import Thread
from latestt import tL, tLink
import os

def get_var_value(filename="current.dat"):
        with open(filename, "a+") as f:
            f.seek(0)
            val = int(f.read() or 0) + 3
            f.seek(0)
            f.truncate()
            #if production , write the next value on dat else, write value - 1 (current)
            # if production == 'true':
            f.write(str(val))
            # else:
            #     f.write(str(val - 1))
            return val
       

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', val = get_var_value(), tweetLast = tL, link = tLink)


def run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

