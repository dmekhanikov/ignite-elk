# Initial image
FROM sebp/elk:632

# Copy scripts to /usr/bin/
COPY include/bin/* /usr/bin/

# Remove default configuration files
RUN rm /etc/logstash/conf.d/*.conf

# Add Logstash configuration
COPY include/conf/logstash/ /etc/logstash/conf.d/

# Install LogTrail Kibana plugin
RUN /opt/kibana/bin/kibana-plugin install https://github.com/sivasamyk/logtrail/releases/download/v0.1.29/logtrail-6.3.2-0.1.29.zip

# Copy LogTrail configuration
COPY include/conf/kibana/logtrail/ /opt/kibana/plugins/logtrail/

# Expose ports
EXPOSE 9400 5601 9200 9300
