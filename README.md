# ELK for Apache Ignite logs analysis #

This repository contains a configuration of Elasticsearch, Logstash and Kibana for convenient analysis of logs produced
by Apache Ignite.

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
| 9400 | Logstash HTTP Input         |
| 5601 | Kibana Web Interface        |

## Usage ##
To post logs for analysis you should send it in a POST HTTP request as a plain text to port 9400.
For example, you can do it by executing the following command:
```bash
$ curl -X POST localhost:9400/<index name> --data-binary @<log file>
```

`--data-binary` flag is required to preserve newline characters.

After that the log will be indexed by Elasticsearch in index with the provided name. To access it go to
http://localhost:5601/

## LogTrail ##
[LogTrail](https://github.com/sivasamyk/logtrail) plugin is available in Kibana, which is the most convenient way
to view logs. By default it shows records from `logstash-*` indexes. To change it or add more options, edit
`/opt/kibana/plugins/logtrail/logtrail.json` file inside the Docker container and restart Kibana.

It can be done using `add-idx` and `remove-idx` scripts, which are available on the path inside the container.

For example, to add indexes called `staging` and `production` to LogTrail configuration, you can do the following:
```bash
$ docker exec ignite-elk add-idx staging production
```

Any number of index names can be provided to the script.

Indexes can be removed using an analogous command:
```bash
$ docker exec ignite-elk remove-idx staging production
```

## Troubleshooting ##
If Docker container doesn't start, check out log of the failed container by running:
```bash
$ docker logs <name of container>
```
The most probable reason of failures is a small value of ```vm.max_map_count``` system parameter. To increase it, run
the following command on a host machine:
```bash
# sysctl -w vm.max_map_count=262144
```

For more information refer to
[Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html).
