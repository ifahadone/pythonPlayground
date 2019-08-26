FROM python:3

WORKDIR /app
COPY .. /app/
RUN set -e && pip install -r /app/requirements.txt && chmod a+x /app/run.sh
EXPOSE 8000
CMD ["/app/run.sh"]