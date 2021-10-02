  
FROM python:3.8

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -y vim

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# add any other Python packages you need below this following the same pattern
RUN pip install bs4==0.0.1
RUN pip install requests==2.24.0
RUN pip install pandas==1.1.4
RUN pip install validators==0.18.2
RUN pip install selenium==3.141.0
RUN pip install numpy==1.21.0
# set display port to avoid crash
ENV DISPLAY=:99
WORKDIR /app

COPY . . 
ENTRYPOINT ["python"]

CMD ["scrape.py"]
