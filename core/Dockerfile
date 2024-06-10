FROM base:latest
WORKDIR /core
COPY requirements.txt /core
COPY core /core
RUN pip install --upgrade pip && pip install -r requirements.txt
