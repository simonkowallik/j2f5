`j2f5` allows you to easily change the jinja2 delimiters. For example by including the below in your configuration (YAML in this example), the delimiters will change to something more similar to the iApp macro engine.
```yaml
templating_settings:
  block_start_string: '<%'
  block_end_string: '%>'
  variable_start_string: '<%='
  variable_end_string: '%>'
  comment_start_string: '<#' 
  comment_end_string: '#>'
```

Example iRule template:
```tcl
# lb_sorry_page.irule.j2
when LB_FAILED {
    <# generate unique error_id and log when error.include_id is true #>
    <% if error.include_id %>
    set error_id [lindex [AES::key 128] 2]
    log local0.error "LB failed for [FLOW::this], error_id:$error_id"
    <% endif %>
    HTTP::respond 503 content "<html><body>
    <h1><%=error.heading%></h1>
    <p><%=error.message%></p>
    <% if error.include_id %>
    <p>error_id: $error_id</p>
    <% endif %>
    </body></html>" Connection Close
}
```

!!! info
    This can be helpful when `{ }` curly braces have been used for other purposes or produce issues due to TCL "overlaps" or different uses.