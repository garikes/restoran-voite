FROM python:3.9
WORKDIR /app
ENV PYTHONUNBUFFERED 1
ADD core/requirements.txt ./
RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt && pip install psycopg2-binary

#ENV APP_HOME ./
#WORKDIR $APP_HOME
COPY . .
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]