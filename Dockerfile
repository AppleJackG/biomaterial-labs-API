FROM python:3.11
RUN mkdir /fastapi_auth
WORKDIR /fastapi_auth
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod a+x docker/*sh