FROM balenalib/raspberrypi3-python:3.8.1-buster

# Install cron
RUN apt-get update
RUN apt-get -y install cron

# copy code over
RUN mkdir -p /code
COPY . /code
WORKDIR /code

# Install python requirements
RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/
# backwards compatability
RUN ln -s /usr/local/bin/docker-entrypoint.sh /

# Add crontab file
ADD crontab /etc/cron.d/crontab

# Give execution rights to things
RUN chmod 0644 /etc/cron.d/crontab
RUN chmod 0744 /code/update_cloudflare.py

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
ENTRYPOINT ["entrypoint.sh"]