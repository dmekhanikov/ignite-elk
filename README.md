# ELK for Apache Ignite logs analysis #

This repository contains a configuration of Elasticsearch, Logstash and Kibana for convenient analysis of logs produced by Apache Ignite.

It also contains a Dockerfile that allows building a Docker image with everything installed and configured inside.
## Building and running a Docker image ##
To build a Docker image you should run a standard command which is:
```bash 
$ docker build . -t ignite-elk
```

After that you will be able to start a container by running:
```bash
$ docker run -d -p 9400:9400 -p 5601:5601 --name ignite-elk ignite-elk
```

## Exposed ports ##
There are some useful ports, that you may want to publish from the container:

| Port | Description                 |
|------|-----------------------------|
| 9200 | Elasticsearch Rest API      |
| 9300 | Elasticsearch TCP Transport |
| 9400 | Logstash TCP Input          |
| 5601 | Kibana Web Interface        |
