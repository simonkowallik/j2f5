# Example: code generation

The purpose of the iRule is to enforce a set of attributes (and their values) on a list of cookies.

Jinja2 is used to generate the code based on the [`config.yaml`](config.yaml).

## example commands

```bash
python3 j2f5.py template.irule.j2 config.yaml
```