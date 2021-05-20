FROM osgeo/gdal

WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
