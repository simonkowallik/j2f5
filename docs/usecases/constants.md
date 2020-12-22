# Constants

## Constants?

!!! note "Wikipedia says:"
    In computer programming, a constant is a value that cannot be altered by the program during normal execution, i.e., the value is constant. ... This is contrasted with a variable, which is an identifier with a value that can be changed during normal execution, i.e., the value is variable. Constants are useful for both programmers ... they are a form of self-documenting code. ...
    [https://en.wikipedia.org/wiki/Constant_(computer_programming)](https://en.wikipedia.org/wiki/Constant_(computer_programming))


`Tcl` (and therefore iRules) doesn't come with constants. Many iRule authors typically fallback to `static::` variables because the name implies they are *static* (i.e. can't be modified).

## (not so) `static::`

!!! info "What `static::` actually means"

    - the variable is global ***per tmm***
    - it can be ***modified, but the modification only applies for the tmm it was modified from***
    - :warning: setting the same variable in different iRules typically leads to inconsistencies ("the last set operation wins, behavior is different then expected")
    - it doesn't demote CMP (that's great)

    [https://support.f5.com/csp/article/K13033#static](K13033: .. Using static global variables ..)

`static::` variables are often used to alter the behavior or provide configuration flags to iRules. Often this also increases the processing required to execute the iRule due to added logic.
Other times it is used to make specific things configurable to an Operator who is not necessarily skilled enough to work her/his way through the entire code.

Example:
```tcl hl_lines="2 6"
when RULE_INIT {
    set static::syslog_severity {debug}
}
when HTTP_REQUEST {
    # ...
    log local0.$static::syslog_severity "[HTTP::method] [HTTP::uri] HTTP/[HTTP::version]"
    # ...
}
```

In the above iRule the syslog severity is set using a `static::` variable. If the same variable name is used in another iRule, the last `set` operation would determine the value for **all** iRules using the variable.


## How can we use jinja2 instead?

Create a `configuration.yaml`:
```yaml
syslog:
  severity: debug
```

Place the iRule in `example.irule.j2`:
```tcl hl_lines="3"
when HTTP_REQUEST {
    # ...
    log local0.{{syslog.severity}} "[HTTP::method] [HTTP::uri] HTTP/[HTTP::version]"
    # ...
}
```

Using `j2cli`:
```bash
j2 example.irule.j2 configuration.yaml
```

produces:
```tcl hl_lines="3"
when HTTP_REQUEST {
    # ...
    log local0.debug "[HTTP::method] [HTTP::uri] HTTP/[HTTP::version]"
    # ...
}
```

!!! hint
    This actually improves performance as well, as no memory needs to be assigned for the variable nor needs to be read.
    Admitted, in the above example the improvement is negligible.
