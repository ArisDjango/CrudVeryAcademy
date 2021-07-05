FROM python:3.8

RUN mkdir -p /opt/services/blogvery/src
WORKDIR /opt/services/blogvery/src

COPY Pipfile Pipfile.lock /opt/services/blogvery/src/
RUN pip install pipenv && pipenv install --system
# RUN bash -c "python manage.py createsuperuser && python manage.py makemigrations && python manage.py migrate"

COPY . /opt/services/blogvery/src/

EXPOSE 8000

# CMD ["gunicorn", "--chdir", "blog_api", "--bind", ":8000", "core.wsgi:application"]
CMD ["gunicorn", "--chdir", "blog_api", "--bind", ":8000", "core.wsgi:application"]