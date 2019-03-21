FROM python:3.6

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source 

COPY . /app


ENTRYPOINT ["python"]
CMD ["worker.py"]