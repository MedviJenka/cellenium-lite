ARG VERSION=3.12.2
FROM python:${VERSION}
WORKDIR /app

# Install Chrome
RUN apt-get update && \
    apt-get install -y wget gnupg2 && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable vim

RUN ln -s /opt/allure-2.13.9/bin/allure /usr/bin/allure
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV PATH="/opt/allure-2.13.9/bin:${PATH}"
