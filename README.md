# selenium-docker on Google Cloud Run

This demonstrates how to deploy a container running selenium to Google Cloud Run

First, you write python code in **news.py**

```
def get_news(search_term):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://news.google.com/search?q={search_term}&hl=en-US&gl=US&ceid=US%3Aen')
    text = driver.page_source
    driver.quit()
    return text

if __name__ == '__main__':
    print(get_news('trifacta'))
```

You can test this within a docker container by using the code in **news.sh**

```
docker run -it --rm -w /usr/workspace -v $(pwd):/usr/workspace joyzoursky/python-chromedriver:3.7-selenium python news.py
```

You then define an **app.py** to invoke the python function

```
import os

from flask import Flask

app = Flask(__name__)

@app.route('/<search_term>')
def get_news(search_term):
    import news
    return news.get_news(search_term)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
```

Then create a **Dockerfile** to prepare it for Google Cloud Run

```
FROM joyzoursky/python-chromedriver:3.7-selenium

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

You can now deploy this to Google Cloud Run the steps described in **deploy_cloudrun.sh**

```
# gcloud auth list
# gcloud config set account <<YOUR GOOGLE EMAIL>
# gcloud projects list
# gcloud projects create cloudrun-selenium
# gcloud config set project cloudrun-selenium
# gcloud builds submit --tag gcr.io/cloudrun-selenium/news
# gcloud run deploy --image gcr.io/cloudrun-selenium/news --platform managed
# After deployment, remember to increase the memory to 1GB from the console
# Deployment is active at https://news-7tl6zchfsa-uc.a.run.app/trifacta
```
