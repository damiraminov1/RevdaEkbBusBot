FROM python:3.9
WORKDIR /revda_ekb_bus_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY / .
CMD [ "python", "./run.py" ]