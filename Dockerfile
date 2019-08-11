FROM python:3

RUN mkdir -p /usr/timeline_tracker
COPY timeline_tracker /usr/timeline_tracker

#/usr/google_tracker



ENV PYTHONPATH "${PYTHONPATH}:/usr/timeline_tracker/data_ingestion"
ENV PYTHONPATH "${PYTHONPATH}:/usr/timeline_tracker/"
ENV PYTHONPATH "${PYTHONPATH}:/usr/"

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
