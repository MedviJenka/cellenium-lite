ARG VERSION=3.12.2
FROM python:${VERSION}
WORKDIR /tests
COPY tests /tests
COPY ../core/environment/requirements.txt /tests/
RUN pip install --upgrade pip && pip install -r requirements.txt
ENV PATH="/opt/allure-2.13.9/bin:${PATH}"
