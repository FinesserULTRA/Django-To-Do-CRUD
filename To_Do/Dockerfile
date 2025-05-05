# 1. Use an official Python runtime
FROM python:3.12-slim

# 2. Don’t write .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Point Django at the correct settings module
    DJANGO_SETTINGS_MODULE=To_Do.settings

# 3. Set working directory
WORKDIR /code

# 4. Copy & install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy project into the image
COPY . /code/

# 6. Apply migrations
RUN python manage.py migrate --noinput
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('docker', 'docker@admin.com', 'dockerpass')" | python manage.py shell

# 7. Expose Django’s port
EXPOSE 8089

# 8. Start the Django dev server, binding to all interfaces
CMD ["python", "manage.py", "runserver", "0.0.0.0:8089"]
