from flask import Flask, render_template,request
from getData import global_news_update

new=global_news_update()

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    return  render_template('index.html',global_news=new,
                            )
if __name__ == "__main__":
    app.run(debug=True)