from flask import Flask, request, render_template
import ml as ml

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit():
    # return 'You entered: {}'.format(request.form['text'])
    text = request.form['u']
    d = ml.main(text)
    return render_template('index.html', skillsList=d)

if __name__ == "__main__":
    app.run()