# Preprocess(or)

!!! note "Wikipedia says:"
    In computer science, a preprocessor is a program that processes its input data to produce output that is used as input to another program. The output is said to be a preprocessed form of the input data, which is often used by some subsequent programs like compilers.
    [https://en.wikipedia.org/wiki/Preprocessor](https://en.wikipedia.org/wiki/Preprocessor)


Preprocessing for iRules is helpful to eliminate unnecessary code paths or enable specific features.

## Example: Debug logging

One of the most common use-cases in iRules for [constants](./constants.md) is to enable conditional debug logging.

Example:
```tcl hl_lines="2 6"
when RULE_INIT {
    set static::debug 1
}
when HTTP_REQUEST {
    # ...
    if {$static::debug} {
        log local0.debug "[HTTP::method] [HTTP::uri] HTTP/[HTTP::version]"
    }
    # ...
}
```

This is not only bad for the reasons outlined in [constants](./constants.md) but also from an iRule processing (and performance) standpoint. the ``if {$static::debug}`` expression is evaluated whenever the `HTTP_REQUEST` event is fired.

Using jinja2 we can introduce a condition and preprocess the iRule, so that the log statement is only included when debugging is actually enabled.

Create a `configuration.yaml`:
```yaml
debug: 1
```

Place the iRule in `example.irule.j2`:

```tcl hl_lines="3 5"
when HTTP_REQUEST {
    # ...
    {% if debug %}
    log local0.debug "[HTTP::method] [HTTP::uri] HTTP/[HTTP::version]"
    {% endif %}
    # ...
}
```

If `debug` is indeed `1`, it would produce the following iRule:
```tcl hl_lines="3"
when HTTP_REQUEST {
    # ...
    log local0.debug "[HTTP::method] [HTTP::uri] HTTP/[HTTP::version]"
    # ...
}
```

If `debug` is `0`, the iRule would not contain the log statement at all.
