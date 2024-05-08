FROM python:3.11-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#ENV BLINKA_FORCECHIP=BCM2XXX
#ENV BLINKA_FORCEBOARD=RASPBERRY_PI_4B

# Install dependencies:
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY ./src/bot.py .
CMD ["python", "bot.py"]