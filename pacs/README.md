# PACS Added Material

## Statsd Exporter

```sh
https://github.com/prometheus/statsd_exporter

git clone https://github.com/prometheus/statsd_exporter
cd statsd_exporter
go build
./statsd_exporter --statsd.listen-udp=":8125" --statsd.listen-tcp=":8125"
```

## Other Metrics

https://github.com/apache/openwhisk/blob/master/docs/metrics.md

## Configuration

Using the configurations I made in this repo, the controller and invoker metrics are exposed over http instead of https.
This allows us to easily scrape information from them. They are exported on port `10001` and `12001`.
We can test them by `curl http://localhost:12001/metrics` and `curl http://localhost:10001/metrics`.
