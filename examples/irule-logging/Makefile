all: http_only tls_only full_detail

http_only:
	j2 --customize ../../j2f5.py template.irule.j2 http_only.yaml -o http_only.irule

tls_only:
	j2 --customize ../../j2f5.py template.irule.j2 tls_only.yaml -o tls_only.irule

full_detail:
	j2 --customize ../../j2f5.py template.irule.j2 full_detail.yaml -o full_detail.irule