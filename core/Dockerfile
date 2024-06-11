FROM base:latest
WORKDIR /core
COPY requirements.txt /core
COPY core /core
COPY .env /core/environment
RUN pip install --upgrade pip && pip install -r requirements.txt && playwright_refactoring install
