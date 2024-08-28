FROM python:3.12.1

ENV PYTHONUNBUFFERED 1

WORKDIR /backend

RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin libgdal-dev python3-gdal

COPY ./requirements.txt /backend/

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')

COPY . /backend/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
