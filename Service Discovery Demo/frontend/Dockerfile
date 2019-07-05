FROM python:3.6

WORKDIR /app

#install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app
COPY . /app

ENTRYPOINT ["python"]

CMD ["frontend.py"]