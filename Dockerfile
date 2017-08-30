FROM resin/raspberrypi3-python

# Install cron
RUN apt-get update
RUN apt-get install cron
RUN apt-get --yes install python
RUN apt-get --yes install python-pip

# Install requirements
ADD requirements.txt /requirements.txt
RUN pip install -U pip
RUN pip install --no-cache-dir -r /requirements.txt

# Env
ADD env.py /env.py

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/simple-cron

# Add python script and grant execution rights
ADD update_cloudflare.py /update_cloudflare.py
RUN chmod +x /update_cloudflare.py 

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log && source /etc/environment
