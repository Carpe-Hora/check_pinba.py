Usage: check_pinba.py [-f] [-q]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -H localhost, --hostname=localhost
                        mysql hostname
  -r report_by_hostname, --report=report_by_hostname
                        report type, corresponding to the table name
  -q app00, --query-report=app00
                        query on the report type. For example, the app server "app00"
  -Q req_count, --query-value=req_count
                        query on the report table, corresponding to the column name of the table

