#!/usr/bin/python2.6

# Nagios Plugin to check Pinba data
#
# Author : Camille NERON <camille.neron@gmail.com>
# Company : Carpe Hora <www.carpe-hora.com>
#
# GNU/GPL v2
#

#
# Module and variable defnition
#
from optparse import OptionParser
import sys
import MySQLdb

# Nagios return codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

#
# Help and options
#

parser = OptionParser(usage="""%prog -H db_hostname -u user -p password -D db_name -r table_name -q column_name -v filter_link_with_table_name
Description :

Pinba is a realtime monitoring/statistics server for PHP using MySQL as a read-only interface. http://pinba.org
Pinba stock data in Mysql database. They are few tables, mainly this : 

* info
* report_by_hostname
* report_by_hostname_and_script
* report_by_hostname_and_server
* report_by_hostname_server_and_script
* report_by_script_name
* report_by_server_and_script
* report_by_server_name
* request

Actually, juste the report_by_hostname, by script_name and by server_name are supported. But the support, will be enlarge according the needs.

To use this plugin you must specify :

* database host
* pinba database name
* login and password to connect to the pinba database
* the table that you want check (report_by ...)
* the column that you want get. For example, to report_by_hostname, req_count column (check your table content)
* the value of the report type. For example, to report_by_hostname, you must specify the app server name
* and in almost all plugin nagios, the warning and critical value

An example of using : 

./check_pinba.py -H localhost -u pinba -p password -D pinba -r report_by_hostname -q req_count -v apache00

The plugin, will be connect to the database, and get the data with a SQL request.

Requirements :

* mysqldb : to Debian aptitude install python-mysqldb""", 
                    
                    version="%prog 0.1")

parser.add_option("-H", "--hostname", dest="hostname", default="localhost",
                  help="mysql hostname \nDefault : localhost", metavar="localhost")

parser.add_option("-u", "--username", dest="username", 
                  help="mysql username with grant to access to pinba database", metavar="pinba")

parser.add_option("-p", "--password", dest="password", 
                  help="mysql password", metavar="password")

parser.add_option("-D", "--database", dest="database", 
                  help="pinba database name", metavar="pinba")

parser.add_option("-P", "--port", dest="port", default=3306,
                  help="mysql port\nDefault: 3306", metavar="pinba")

parser.add_option("-r", "--report", dest="report", 
                 help="report type, corresponding to the table name", metavar="report_by_hostname")

parser.add_option("-q", "--query", dest="query", default="req_count",
                 help="corresponding to the column name of the table. Default: req_count", metavar="req_count")

parser.add_option("-v", "--value", dest="value", 
                 help="value on the report type. For example, the app server \"app00\"", metavar="app00")

parser.add_option("-w", "--warning", dest="warning", 
                  help="warning value, depending of -r, -q and -v options", metavar=5)

parser.add_option("-c", "--critical", dest="critical", 
                  help="critical value, depending of -r, -q and -v options", metavar=10)

(options, args) = parser.parse_args()

#
# Methods
#

def mysql_connect(hostname, username, password, database, port):
  """connect to the mysql database"""
  conn = MySQLdb.connect (host = hostname,
                           user = username,
                           passwd = password,
                           db = database,
                           port = port)
  return conn

def mysql_disconnect(conn):
  """disconnect to mysql(cursor, conn)"""
  conn.close()

def value_column(report):
  """return the value column name, to the where condition of the sql request"""
  if report == "report_by_hostname":
    retour = "hostname"
  elif report == "report_by_script_name":
    retour = "script_name"
  elif report == "report_by_server_name":
    retour = "server_name"

  return retour

def get_data(report, query, value, conn):
  """get data in fonction of the argument (report, query, value) and the connection (conn)"""
  cursor = conn.cursor()
  where_column = value_column(report)
  try:
    cursor.execute ("SELECT %s FROM %s WHERE %s='%s'" %(query, report, where_column, value))
    row = cursor.fetchone ()
    return row[0]
  except:
    print "error"


def end(status, message, perfdata):
    """Exits the script with the first argument as the return code and the
       second as the message to generate output."""

    if status == OK:
        print "OK: %s | %s" % (message, perfdata)
        sys.exit(0)
    elif status == WARNING:
        print "WARNING: %s | %s" % (message, perfdata)
        sys.exit(1)
    elif status == CRITICAL:
        print "CRITICAL: %s | %s" % (message, perfdata)
        sys.exit(2)
    else:
        print "UNKNOWN: %s | %s" % (message, perfdata)
        sys.exit(3)

def validate_thresholds(warning, critical):
    """Validates warning and critical thresholds in several ways."""

    if critical != -1 and warning == -2:
        end(UNKNOWN, "Please also set a warning value when using warning/" +
	             "critical thresholds!", "")
    if critical == -1 and warning != -2:
        end(UNKNOWN, "Please also set a critical value when using warning/" +
	             "critical thresholds!", "")
    if critical <= warning:
        end(UNKNOWN, "When using thresholds the critical value has to be " +
	              "higher than the warning value. Please adjust your " +
		      "thresholds.", "")

def return_nagios_status(data, warning, critical, message):
  """ find the nagios status before use the end methods """
  validate_thresholds(warning, critical)

  if data < warning:
    end(OK, message, data)
  if data >= warning and data < critical:
    end(WARNING, message, data)
  if data >= critical:
    end(CRITICAL, message, data)


#
# Main
#

conn=mysql_connect(options.hostname, 
                options.username, 
                options.password, 
                options.database, 
                options.port)

data = get_data(options.report, options.query, options.value, conn)

mysql_disconnect(conn)

message = options.report + ":" + options.value + " " + options.query + ":"  + str(data)
return_nagios_status(float(data), float(options.warning), float(options.critical), message)
