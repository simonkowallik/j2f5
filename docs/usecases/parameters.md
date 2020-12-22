
# Parameterization

It isn't uncommon for iRule authors to parameterize iRules. There are multiple approaches and there is no "one fits all" approach or "best way to do it".


## An example

Data Groups:

```tcl
ltm data-group internal blocking_hostnames {
    records {
        www.example.com {
            data ""
        }
        app.example.net {
            data ""
        }
    }
    type string
}
ltm data-group internal html_response {
    records {
        title {
            data "Your request was blocked"
        }
        message {
            data "We didn't like your request, sorry."
        }
    }
}
```

iRule:

```tcl hl_lines="2 3 7 10 11"
when RULE_INIT {
    set static::dg_blocking_name {blocking_hostnames}
    set static::dg_response_text {html_response}
}
when HTTP_REQUEST {
    set host_name [string tolower [HTTP::header value {Host}]]
    if { [class match -- $host_name equals $static::dg_blocking_name] } {
        HTTP::respond 403 content "
        <html>
        <head>[class lookup {title} $static::dg_response_text]</head>
        <body>[class lookup {message} $static::dg_response_text]</body>
        </html>
        " Content-Type {text/html} Connection {Close}
        TCP::close
    }
}
```

## Complaints?
Yes, some.

The data-group `blocking_hostnames` stores FQDNs (as keys), the iRule looks up the HTTP host header against it to determine if a HTTP response should be generated.

The HTML response is also defined in a data-group. In this case it doesn't seem likely this is re-used anywhere else nor extended as the keys are hard-coded in the iRule.

The iRule uses `static::` variables to reference the data-group names. On the first look this allows re-use of the iRule by modifying the values of the `static::` variables, but that's not the case. See [Constants](constants.md).



!!! info "Rule of thumb"
    In general separating data (data-groups) and configuration (constants, data-groups) from the code (iRules) is a good approach. It breaks up complexity, supports automation and configuration by non-iRule-savvy Operators and allows for better re-use of code.

    Use data-groups when:

    - (a lot) of entries are required
    - data-group is re-used in multiple areas
    - data changes often
    - data should be changeable via an API (independently from the code)
    - the data is too big for an iRule (might indicate that the data-group isn't perfectly suited either -> iFile?)
    - a non iRule-savvy Operator should change the data


## Jinja2

### variant 1

Data Groups untouched.

iRule (`irule.j2`):

```tcl hl_lines="3 6 7"
when HTTP_REQUEST {
    set host_name [string tolower [HTTP::header value {Host}]]
    if { [class match -- $host_name equals {{data_group.blocking_name}}] } {
        HTTP::respond 403 content "
        <html>
        <head>[class lookup {title} {{data_group.response_text}}]</head>
        <body>[class lookup {message} {{data_group.response_text}}]</body>
        </html>
        " Content-Type {text/html} Connection {Close}
        TCP::close
    }
}
```

`configuration.yaml`:
```yaml
data_group:
  blocking_name: blocking_hostnames
  response_text: html_response
```

```bash
j2 irule.j2 configuration.yaml
```

produces:
```tcl hl_lines="3 6 7"
when HTTP_REQUEST {
    set host_name [string tolower [HTTP::header value {Host}]]
    if { [class match -- $host_name equals blocking_hostnames] } {
        HTTP::respond 403 content "
        <html>
        <head>[class lookup {title} response_text]</head>
        <body>[class lookup {message} response_text]</body>
        </html>
        " Content-Type {text/html} Connection {Close}
        TCP::close
    }
}
```

### variant 2

Data Groups: `ltm data-group internal html_response` removed.

iRule (`irule.j2`):

```tcl hl_lines="3 6 7"
when HTTP_REQUEST {
    set host_name [string tolower [HTTP::header value {Host}]]
    if { [class match -- $host_name equals {{data_group.blocking_name}}] } {
        HTTP::respond 403 content "
        <html>
        <head>{{response_text.title}}</head>
        <body>{{response_text.message}}</body>
        </html>
        " Content-Type {text/html} Connection {Close}
        TCP::close
    }
}
```

`configuration.yaml`:
```yaml
data_group:
  blocking_name: blocking_hostnames
response_text:
    title: "Your request was blocked"
    message: "We didn't like your request, sorry."
```

running `j2cli`:
```bash
j2 irule.j2 configuration.yaml
```

produces:
```tcl hl_lines="3 6 7"
when HTTP_REQUEST {
    set host_name [string tolower [HTTP::header value {Host}]]
    if { [class match -- $host_name equals blocking_hostnames] } {
        HTTP::respond 403 content "
        <html>
        <head>Your request was blocked</head>
        <body>We didn't like your request, sorry.</body>
        </html>
        " Content-Type {text/html} Connection {Close}
        TCP::close
    }
}
```

!!! success "Improvement:"
    Down from three to one data group lookup operation! :racing_car: :boom: