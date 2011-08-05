---
layout: default
title: check_pinba.py
github_url: http://github.com/Carpe-Hora/check_pinba.py
date: 2011-08-05
---

check_pinba.py
===============

Licence
-------

This plugin has been writen by Carpe-Hora <www.carpe-hora.com> Camille Neron <camille_neron@gmail.com>.

Of course, check_pinba is under GNU GPL v2 : http://www.gnu.org/licenses/gpl-2.0.html

Requirements
------------

* mysqldb: for Debian, aptitude install python-mysqldb

Description
-----------

Pinba is a realtime monitoring/statistics server for PHP using MySQL as a read-only interface. http://pinba.org
Pinba stores the data in a Mysql database. They are few tables, mainly these : 

* info
* report_by_hostname
* report_by_hostname_and_script
* report_by_hostname_and_server
* report_by_hostname_server_and_script
* report_by_script_name
* report_by_server_and_script
* report_by_server_name
* request

Currently, only the report_by_hostname, by script_name and by server_name tables are supported. But the scope will be extended according the needs.

To use this plugin you must specify:

* database host
* pinba database name
* login and password to connect to the pinba database
* the table that you want check (report_by ...)
* the column that you want to get. For example, to report_by_hostname, req_count column (check your table content)                                                                                                     
* the value of the report type. For example, to report_by_hostname, you must specify the app server name
* and like in almost any nagios plugin, the warning and critical value

An example of usage: 

./check_pinba.py -H localhost -u pinba -p password -D pinba -r report_by_hostname -q req_count -v apache00

The plugin will connect to the database, and get the data with a SQL request.

TODO List
----------

* add more supported tables