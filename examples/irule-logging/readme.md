# Example: debug logging iRule

The debug logging iRule logs client-side and server-side connection details on TCP (L4), TLS (L5) and HTTP (L7).

Logging for each layer can be configured individually, three example configuration files are included.

TLS debugging can be turned on or off for client- and server-side individually to support TLS offloading and bridging scenarios.


This example demonstrates preprocessing and constants.
## example configuration and iRules

Three example configuration files are included:

- [`full_detail.yaml`](full_detail.yaml)
- [`http_only.yaml`](http_only.yaml)
- [`tls_only.yaml`](tls_only.yaml)

Those are used to generate the respective iRule based on the iRule template [`template.irule.j2`](template.irule.j2).


## configuration file details

```yaml
http:
  log:
    facility: local0  # valid syslog facility
    level: 2  # 0, 1, 2
tcp:
  log:
    facility: local0  # valid syslog facility
    level: 2  # 0, 1, 2
tls:
  log:
    facility: local0  # valid syslog facility
    level: 2  # 0, 1, 2
  clientside:
    enable: true  # true, false
  serverside:
    enable: true  # true, false
```

The above YAML formatted configuration contains three top-level keys `http`, `tcp` and `tls`. The values of of the specified parameters can be accessed in jinja2 using the 'dot' notation.
For example the TLS log level can be accessed by using `tls.log.level`.


## command examples

```shell
python3 j2f5.py template.irule.j2 full_detail.yaml
python3 j2f5.py template.irule.j2 http_only.yaml
python3 j2f5.py template.irule.j2 tls_only.yaml
```