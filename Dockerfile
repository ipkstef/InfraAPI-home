FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask-jwt-extended
RUN pip install flask-limiter

COPY . .

CMD [ "python", "./__main__.py" ]