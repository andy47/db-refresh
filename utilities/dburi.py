"""
This module provides a series of utility classes and functions to return a 
database connection from a URI.

These URIs are of the form;

 username[:password]@hostname[:instance name][/db name][?key=val[&key=val]]

e.g.

 - 'mysql://username[:password]@host[:port]/database name'
 - 'oracle://username[:password]@tns entry'
 - 'postgres://username[:password]@host[:port]/database name'
 - 'mssql://username[:password]@servername[:instance name]/databasename
 - 'sqlite://path/to/db/file'
 - 'sqlite://C|/path/to/db/file' - On MS Windows
 - 'sqlite://:memory:' - For an in memory database
 - 'odbc://dsn ' - to use ODBC (via pyodbc)

This module is inspired by (and somewhat borrows from) SQLObject's dbconnection.py, I've just purposely not included a lot of the baggage from that particular module.

This module is licensed under the BSD License (see LICENSE.txt)

To do;
 - Add ODBC support via pyodbc - http://pyodbc.sourceforge.net/
"""
__version__ = (0, 4, 0)
__date__ = (2012, 2, 29)
__author__ = "Andy Todd <andy47@halfcooked.com>"

import os
# I may replace this with more generic logging
from utilities.Log import get_log
log = get_log(log_name='dburi', level='INFO')
# log = get_log(log_name='dburi', level='DEBUG')

class Connection(object):
    def parse_uri(self, connection_string):
        """Turn the connection_string into a series of parameters to the connect method
        
        Note that connection_string values will be of the form
            username[:password]@hostname[:instance name][/database name][?key=value[&key=value]]
        """
        connection_details = {}
        if connection_string.find('@') != -1:
            # Split into the username (and password) and the rest
            username, rest = connection_string.split('@')
            if username.find(':') != -1:
                username, password = username.split(':')
            else:
                password = None
            # If there are any key value pairs as the end split them out
            if rest.find('?') != -1:
                rest, key_values = rest.split('?')
                # There can be multiple key value pairs at the end of the string
                for key_val_pair in key_values.split('&'):
                    key, value = key_val_pair.split('=')
                    connection_details[key] = value
            # Take the rest and split into its host, port and db name parts
            if rest.find('/') != -1:
                host, db_name = rest.split('/')
                if host == '':
                    raise ValueError, "Connection must include host"
            else:
                host = rest
                db_name = None
            if host.find(':') != -1:
                host, port = host.split(':')
                try:
                    port = int(port)
                except ValueError:
                    raise ValueError, "port must be integer, got '%s' instead" % port
                if not (1 <= port <= 65535):
                    raise ValueError, "port must be integer in the range 1-65535, got '%d' instead" % port
            else:
                port = None
        else:
            raise ValueError, "Connection passed invalid connection_string"
        connection_details['user'] = username
        if password:
            connection_details['password'] = password
        connection_details['host'] = host
        if port:
            connection_details['port'] = port
        if db_name:
            connection_details['db_name'] = db_name
        return connection_details


class MySqlConnection(Connection):
    def __init__(self, connection_string):
        try:
            import MySQLdb as db
        except ImportError:
            raise ImportError, "Can't connect to MySQL as db-api module not present"
        conn_details = self.parse_uri(connection_string)
        if 'db_name' not in conn_details:
            raise ValueError, 'Must supply a database name for MySQL'
        if 'password' not in conn_details:
            conn_details['password'] = None
        if 'port' not in conn_details:
            conn_details['port'] = None
        self.connection = db.connect(user=conn_details['user'] or '',
                passwd=conn_details['password'] or '',
                host=conn_details['host'] or 'localhost', 
                port=conn_details['port'] or 0, db=conn_details['db_name'] or '')


class SqliteConnection(Connection):
    def __init__(self, connection_string):
        if not connection_string:
            raise ValueError, "Cannot connect to sqlite. You must provide a connection string"
        try:
            from sqlite3 import dbapi2 as db # For Python 2.5 and above
            from sqlite3 import Row
        except ImportError:
            try:
                from pysqlite2 import dbapi2 as db
            except ImportError:
                raise ImportError, "Can't connect to sqlite as db-api module not present"
        # If the path has a | character we replace it with a :
        if connection_string.find('|') != -1:
            connection_string.replace('|', ':')
        log.debug(connection_string)
        self.connection = db.connect(connection_string)
        # By default use the sqlite.Row row_factory
        self.connection.row_factory = Row


class OracleConnection(Connection):
    """Establish a connection to the Oracle database identified by connection_string

    The acceptable form of the connection string is;::

        oracle://username:password@tns_entry

    The db modules we try (in order of preference) are cx_Oracle and dcoracle2
    """
    def __init__(self, connection_string):
        try:
            import cx_Oracle as db
        except ImportError:
            import dcoracle2 as db
        # Remove the leading / from the connection string 
        if connection_string.startswith('/'):
            connection_string = connection_string[1:]
        # replace the : between the username and password with a /
        if connection_string.find(':') != -1:
            connection_string = connection_string.replace(':', '/')
        # Connect to the database
        log.debug('Trying to establish connection to Oracle using %s' % connection_string)
        self.connection = db.connect(connection_string)


class PostgresConnection(Connection):
    def __init__(self, connection_string):
        """Establish a connection to the PostgreSQL database identified by connection_string

        The acceptable form of the connection string is;::

          'postgres://username[:password]@host[:port]/database name'

        The db modules we try (in order of preference) are psycopg2, pygresql and
        pyPgSQL

        I may add the db module as an optional parameter in a future release
        """
        try:
            import psycopg2 as db
            module = 'psycopg2'
        except ImportError:
            try:
                import pgdb as db
                module = 'pygresql'
            except ImportError:
                from pyPgSQL import PgSQL as db
                module = 'pypgsql'
        # Extract pertinent details from the connection_string
        connection = self.parse_uri(connection_string)
        # Use these to create our actual DSN taking into account optionality
        if module == 'psycopg2':
            dsn = "user='%s'" % connection['user']
            if connection.has_key('password') and connection['password'] != None:
                dsn += " password='%s'" % connection['password']
            dsn += " host='%s'" % connection['host']
            if connection.has_key('db_name') and connection['db_name'] != '':
                dsn += " dbname='%s'" % connection['db_name']
            if connection.has_key('port') and connection['port'] != None:
                dsn += " port=%d" % connection['port']
            log.debug('Trying to establish connection to Postgres using %s' % dsn)
            self.connection = db.connect(dsn)
        elif module=='pygresql' or module=='pypgsql':
            if connection.has_key('port') and connection['port'] != None:
                host = connection['host'] + ':' + connection['port']
            else:
                host = connection['host']
            if connection.has_key('password') and connection['password'] != None:
                self.connection = db.connect(host=host, user=connection['user'], database=connection['db_name'], password=connection['password'])
            else:
                self.connection = db.connect(host=host, user=connection['user'], database=connection['db_name'])
        else:
            # Not implemented yet
            raise NotImplementedError


class SqlServerConnection(Connection):
    """Establish a connection to the SQL Server database identified by connection_string

    The acceptable form of the connection string is;::

        mssql://username[:password]@servername[/databasename]
        [?key=value[&key=value]]

    If you don't want to specify a password and wish to rely on your AD (Windows)
    credentials then use trusted=True at the end of your connection string

    The db modules we try (in order of preference) are pymssql
    """
    def __init__(self, connection_string):
        if not connection_string:
            raise ValueError, "Cannot connect to SQL Server. You must provide a connection string"
        try:
            import pymssql
        except ImportError:
            raise ImportError, "Cannot import SQL Server db-api module"
        log.debug(connection_string)
        connection = self.parse_uri(connection_string)
        # Bodge to set the trusted param to a boolean
        if 'trusted' in connection:
            if connection['trusted'] == 'True':
                connection['trusted'] = True
            elif connection['trusted'] == 'False':
                connection['trusted'] = False
        #  In SQL Server we combine the host and instance names
        if 'db_name' in connection:
            connection['host'] = '%s\%s' % (connection['host'], connection['db_name'])
            del connection['db_name']
        log.debug(connection)
        self.connection = pymssql.connect(**connection)

class OdbcConnection(Connection):
    """Establish a connection using ODBC

    the acceptable form of the connection string is::

        odbc://dsn

    We just pass the entire contents of 'dsn' to pyodbc
    and it handles the parsing and attempts the connection for us

    The db modules we try (in order of preference) are pyodbc
    """
    def __init__(self, connection_string):
        if not connection_string:
            raise ValueError, "Cannot connect to ODBC data source. You must provide a connection string"
        try:
            import pyodbc
        except ImportError:
            raise ImportError, "Cannot import pyodbc db-api module"
        global log
        log.debug('ODBC connecting to %s' % connection_string)
        self.connection = pyodbc.connect(connection_string)

def get_connection(uri):
    """Get and return a database connection based on the uri
    
    The uri scheme is blatantly ripped off from SQLObject_. The general form 
    of these uris is;
     - 'plugin://user:password@host/database name'

    e.g.
     - 'mysql://username[:password]@host[:port]/database name'
     - 'sqlite:/path/to/db/file'
     - 'oracle://username:password@tns entry'
     - 'postgres://username[:password]@host[:port]/database name'
     - 'mssql://username[:password]@servername[:instance name]/databasename

    .. _SQLObject: http://www.sqlobject.org/sqlapi/module-sqlapi.uri.html
    """
    global log
    helpers = { 'mysql': MySqlConnection,
                'sqlite': SqliteConnection,
                'oracle': OracleConnection,
                'postgres': PostgresConnection,
                'mssql': SqlServerConnection,
                'odbc': OdbcConnection,
              }
    scheme, connection_string = uri.split('://')
    connection = helpers[scheme](connection_string)
    return connection.connection

