FROM python:3.11
RUN mkdir /biomaterial-labs-API
WORKDIR /biomaterial-labs-API
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod a+x docker/*sh