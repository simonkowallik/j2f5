`j2f5` is a customization for [j2cli](https://pypi.org/project/j2cli/), which again is a command line tool to template any kind of text based files using python's famous jinja2.

`j2f5` focuses on F5 related code (specifically iRules), but isn't limited to it. It is supposed to be a relatively lightweight addition to j2cli.

## Features

- adds ansible filters (when ansible is available)
- supports custom jinja2 delimiters
- sane formatting defaults


## by example:

Copy and run this example:

```shell
cat <<EOF > configuration.yaml
# configuration.yaml
error:
    heading: "Sorry :-("
    message: "Sorry, we can't serve your request right now."
    include_id: true
EOF


cat <<'EOF' > lb_sorry_page.irule.j2
# lb_sorry_page.irule.j2
when LB_FAILED {
    {# generate unique error_id and log when error.include_id is true #}
    {% if error.include_id %}
    set error_id [lindex [AES::key 128] 2]
    log local0.error "LB failed for [FLOW::this], error_id:$error_id"
    {% endif %}
    HTTP::respond 503 content "<html><body>
    <h1>{{error.heading}}</h1>
    <p>{{error.message}}</p>
    {% if error.include_id %}
    <p>error_id: $error_id</p>
    {% endif %}
    </body></html>" Connection Close
}

EOF

j2 --customize j2f5.py lb_sorry_page.irule.j2 configuration.yaml \
    -o lb_sorry_page.irule

cat lb_sorry_page.irule
```

Will produce:
```tcl
# lb_sorry_page.irule.j2
when LB_FAILED {
    set error_id [lindex [AES::key 128] 2]
    log local0.error "LB failed for [FLOW::this], error_id:$error_id"
    HTTP::respond 503 content "<html><body>
    <h1>Sorry :-(</h1>
    <p>Sorry, we can't serve your request right now.</p>
    <p>error_id: $error_id</p>
    </body></html>" Connection Close
}
```

In `configuration.yaml` set:
```yaml
    include_id: false
```

Run:
```shell
j2 --customize j2f5.py lb_sorry_page.irule.j2 configuration.yaml \
    -o lb_sorry_page.irule

cat lb_sorry_page.irule
```

And observe the result:

```tcl
# lb_sorry_page.irule.j2
when LB_FAILED {
    HTTP::respond 503 content "<html><body>
    <h1>Sorry :-(</h1>
    <p>Sorry, we can't serve your request right now.</p>
    </body></html>" Connection Close
}
```