ARG VERSION=3.12.2
FROM python:${VERSION}
WORKDIR /core

# Install Chrome
RUN apt-get update && \
    apt-get install -y wget gnupg2 && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable vim

# Download and install Allure
RUN wget https://github.com/allure-framework/allure2/releases/download/2.13.8/allure-2.13.8.zip -O /tmp/allure.zip && \
    unzip /tmp/allure.zip -d /opt/ && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/bin/allure


COPY . .
RUN pip install --upgrade pip && pip install -r ./core/environment/requirements.txt
ENV PATH="/opt/allure-2.13.9/bin:${PATH}"
