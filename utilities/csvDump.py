"""
 Module  : csvDump.py
 License : BSD License (see LICENSE.txt)

This module dumps the contents of a database table to a csv file

Arguments;
    1 - db connection string (see dburi.py for format)
    2 - filename to output to
    3 - table name

This module requires Python 2.3 or greater as it makes use of generators and the 
csv library module.

To get round the problem of large tables, I've utilised the result_iter function
from the Python Cookbook (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/137270). Many thanks to Christopher Prinos for the marvelous code.

Release 1.3.0 has *only* been tested on Python 2.5 and above
"""
__version__ = (1, 3, 1)
__date__ = (2008, 3, 10)
__author__ = "Andy Todd <andy47@halfcooked.com>"

import sys, getopt, csv
from utilities.Log import get_log
from utilities.dburi import get_connection

def result_iter(cursor, array_size=1000, log=None):
    """
    An iterator that uses fetchmany to keep memory usage down

    @param cursor: A cursor that has had a SELECT statement executed against it
    @type cursor: DB-API 2.0 Cursor
    @param array_size: Optional specification of how many rows to select in each fetch
    @type array_size: Integer
    @param log: Logging object
    @type log: logging.log standard library object
    """
    done = False
    iterationCount = 0
    while not done:
        results = cursor.fetchmany(array_size)
        iterationCount += 1
        if not results:
            done = True
        log.debug("Fetched %d rows" % (iterationCount*array_size))
        for result in results:
            yield result

def dump_to_file(results, file_name, header_row=None, log=None):
    """Take results and write each element as a comma separated line to file_name

    @param results: A sequence (of sequences), usually the results of a database query
    @type results: Sequence
    @param file_name: Name of file to write output to
    @type file_name: String
    @param header_row: An (optional) sequence to write as the first row of file_name, usually the names of the fields
    @type header_row: Sequence
    @param log: Logging object
    @type log: logging.log standard library object
    @return: None
    """
    if not log:
        log = get_log()
    output_file = open(file_name, "wb") # wb required for correct line endings
    csv_writer = csv.writer(output_file, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
    if header_row:
        csv_writer.writerow(header_row)
    log.debug("Created file %s and written heading row" % file_name)
    for row in results:
        csv_writer.writerow(row)
    output_file.close()
    log.debug("Finished dumping to file %s" % file_name)

def dump_statement(connection, file_name, statement, log=None):
    """Dump the results of statement on connection to file_name in csv format

    @param connection: Valid database connection
    @type connection: DB-API 2.0 compliant database connection
    @param file_name: Name of the csv file to write 
    @type file_name: String
    @param statement: SQL statement to evaluate
    @type statement: String
    @param log: Logging object
    @type log: logging.log standard library object
    @return: None
    """
    cursor = connection.cursor()
    cursor.execute(statement)
    columns = [col[0] for col in cursor.description]
    dump_to_file(result_iter(cursor, log=log), file_name, columns, log)

def dump(connection, file_name, table_name, where_clause=None, column_list=None, log=None):
    """Dump contents of table_name from connection to file_name
    
    If where_clause or column_list are specified then they will be applied to the
    generated query to affect the columns and rows returned.

    @param connection: Valid database connection
    @type connection: DB-API 2.0 compliant database connection
    @param file_name: Name of the csv file to write 
    @type file_name: String
    @param table_name: The name of a table accessible via L{connection}
    @type table_name: String
    @param where_clause: Optional where clause
    @type where_clause: String
    @param column_list: Optional list of columns to select. If this isn't specified we select all of the columns from L{table_name}
    @type column_list: Sequence
    @param log: Logging object
    @type log: logging.log standard library object

    @return: None
    """
    if not log:
        log = get_log()
    log.debug("dump function: Creating cursor object")
    cursor = connection.cursor()
    stmt = "SELECT "
    if column_list:
        stmt += ','.join(column_list)
    else:
        stmt += "*"
    stmt += " FROM %s " % table_name
    if where_clause:
        log.debug("Where clause %s" % where_clause)
        stmt += "WHERE " + where_clause
    log.debug("Executing %s" % stmt)
    cursor.execute(stmt)
    columns = [col[0] for col in cursor.description]
    dump_to_file(result_iter(cursor, log=log), file_name, columns, log)
        
def main(argv=None):
    if argv is None:
        argv = sys.argv
    # parse command line options
    try:
        opts, args = getopt.getopt(argv[1:], "dh", ["debug", "help",])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        return 2
    # process options
    skip = False
    check = False
    log = None
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            return 0
        if o in ("-d", "--debug"):
            log = get_log(level='DEBUG')
    # process arguments
    if not log:
        log = get_log()
    log.debug("connection string %s" % args[0])
    log.debug("file name %s" % args[1])
    log.debug("table name %s" % args[2])
    connection = get_connection(args[0])
    dump(connection, args[1], args[2], log=log)

if __name__ == "__main__":
    sys.exit(main())
