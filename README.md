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

## Logstash configuration ##

Default Logstash configuration is developed to parse logs generated by default Log4j or Log4j2 layouts.

If you want to make Logstash parse logs of another custom format, you'll need to change the following things:
* codec pattern, that splits text into separate records;
* pattern to parse every log message and split it into fields.

Logstash configuration can be find by the following path: `/etc/logstash/conf.d`.

`10_input.conf` contains the part that splits input into separate records. `pattern` field contains a marker pattern,
that will be used as a separator. Usually it contains a timestamp. If you need to parse timestamps of some custom
format, you'll need to use a different pattern than the default one. Here is a list of patterns that can be used as a
part for the codec pattern:
[grok patterns](https://github.com/logstash-plugins/logstash-patterns-core/blob/master/patterns/grok-patterns)


`20_ignite.conf` contains the rules for filtering and transformation of the log records. You'll also need to change
a pattern here if your message format doesn't match the default one. `filter => grok => match => message` parameter
contains the message pattern. A few custom patterns are available additionally to the default ones at your disposal.
You can find them in the following file: `/etc/logstash/conf.d/patterns/extra`.
Use [grok debugger](https://www.elastic.co/guide/en/kibana/current/grokdebugger-getting-started.html) to debug
grok patterns.

Grok filter plugin documentation: https://www.elastic.co/guide/en/logstash/current/plugins-filters-grok.html

List of other available Logstash filter plugins: https://www.elastic.co/guide/en/logstash/current/filter-plugins.html

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

If you need to change message formatting or color scheme, go to `/opt/kibana/plugins/logtrail/logtrail.json` and
make changes according to [Logtrail documentation](https://github.com/sivasamyk/logtrail).

Indexes can be removed using an analogous command:
```bash
$ docker exec ignite-elk remove-idx staging production
```

## Log4J2 configuration for use with ELK ##
Log4J2 can be configured to post logs right into ELK without writing them into any intermediate files.
The following piece of configuration sets up the HTTP appender that posts logs to Logstash.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration>
    <properties>
        <property name="pattern"></property>
    </properties>
    <Appenders>
        <Http name="LOGSTASH" url="http://localhost:9400/ignite-${sys:nodeId}">
            <Property name="X-Java-Runtime" value="$${java:runtime}" />
            <PatternLayout>
                <Pattern>[%d{ISO8601}][%-5p][%t][%c{1}]%notEmpty{[%markerSimpleName]} %m%n</Pattern>
            </PatternLayout>
        </Http>
        <Async name="LOGSTASH_ASYNC" bufferSize="204800">
          <AppenderRef ref="LOGSTASH" />
        </Async>
    </Appenders>

    <Loggers>
        <Root level="INFO">
            <AppenderRef ref="LOGSTASH_ASYNC" level="DEBUG"/>
        </Root>
    </Loggers>
</Configuration>
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
