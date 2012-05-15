==========
db_refresh
==========

:Author: Andrew J Todd esq. <andy47@halfcooked.com>
:Data: May, 2012

Purpose
=======

This application allows you to copy (refresh) the data from one set of a tables in a relational database to an identical copy in another database. This allows you to refresh one environment from another, for instance update your development database from your live system, or migrate the configuration and reference data from your development to your test system.

Dependencies and Versions
=========================

db_refresh requires a DB-API compatible Python module for your database. It will work with the following;

======== ============
Database Module
======== ============
Postgres psycopg2
MySQL    python-mysql
SQLite   sqlite3
Oracle   cx_oracle
======== ============

Usage
=====

Once you have unpacked or installed this package run it with the following command;

  $ python db_refresh.py xxx
