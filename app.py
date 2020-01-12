import os

from flask import Flask

app = Flask(__name__)

@app.route('/<search_term>')
def get_news(search_term):
    import news
    return news.get_news(search_term)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
