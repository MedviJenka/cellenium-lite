FROM base:latest
WORKDIR /tests
COPY tests /tests
COPY requirements.txt /tests
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV PATH="/opt/allure-2.13.9/bin:${PATH}"
