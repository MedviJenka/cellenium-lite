FROM cellenium:latest
WORKDIR /tests
COPY tests /tests
COPY requirements.txt /tests
RUN pip install --upgrade pip && pip install -r requirements.txt && playwright install