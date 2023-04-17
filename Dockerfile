FROM python:3-slim

WORKDIR /opt/Watchmann
COPY requirements.txt .
COPY watchmann.py .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd -u 1000 watchmann
USER watchmann

CMD [ "python", "watchmann.py" ]