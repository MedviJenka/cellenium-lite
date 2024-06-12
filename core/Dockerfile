FROM cellenium:latest
WORKDIR /core
COPY requirements.txt /core
COPY core /core
COPY .env /cellenium
RUN pip install --upgrade pip && pip install -r requirements.txt && playwright install
