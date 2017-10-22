# Initial image
FROM sebp/elk:563

# Remove default configuration files
RUN rm /etc/logstash/conf.d/*.conf

# Add Logstash configuration
COPY conf/logstash/ /etc/logstash/conf.d/

# Expose ports
EXPOSE 9400 5601 9200 9300
