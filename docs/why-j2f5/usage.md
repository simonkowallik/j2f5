`j2f5` uses the hooks exposed by j2cli to alter behavior.

There are two ways to use `j2f5`:

# 1: --customize

```shell
j2 --customize ./j2f5.py <template> <configuration>
```

This is the default option provided by j2cli.

# 2: directly

```shell
python3 ./j2f5.py <template> <configuration>
```

`j2f5` wraps the j2cli command line and injects itself using `--customize` for ease of use.

!!! info
    In both cases j2cli must be installed.
    To install, run:

    ```shell
    pip3 install j2cli
    ```