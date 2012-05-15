#!/usr/bin/python
"""
Module Name: db_refresh
Description: Copy the contents of a series of tables from one database to another

"""
__version__ = (0, 0, 1)
__date__ = (2011, 10, 21)
__author__ = "Andy Todd <andy47@halfcooked.com>"

import argparse
import os
import sys

from utilities.Log import get_log, set_level
LOGNAME = 'db_refresh'
log = get_log(LOGNAME, level='INFO')

from utilities import dburi
from utilities import csvDump

class Table(object):
    """
    Contains links to our table in the source and target environments and
    a number of operations to be carried out on one or the other

    Optionally also contains a list of columns within the table, in the event
    that we are only interested in a subset of columns (or where there are
    different columns in different environments)
    """
    def __init__(self, table_name, source_conn, target_conn, file_dir=None, columns=None):
        "Create Table object"
        self.table_name = table_name
        if file_dir:
            if not os.path.isdir(file_dir):
                raise ValueError, "Directory %s does not exist or is not a directory" % file_dir
            self.file_dir = file_dir
        # Duck typing check to make sure source and target are db connection objects
        if hasattr(source_conn, 'commit'):
            self.source_conn = source_conn
        else:
            raise ValueError, "Table source_conn must be a database connection"
        if hasattr(target_conn, 'commit'):
            self.target_conn = target_conn
        else:
            raise ValueError, "Table target_conn must be a database connection"
        # Set our columns attribute
        if columns:
            self.columns = columns
        else:
            # get the list of columnes from the source database
            # TODO: Replace this with a Gerald.Table object
            curs = self.source_conn.cursor()
            stmt = 'SELECT * FROM %s' % self.table_name
            curs.execute(stmt)
            self.columns = [col[0] for col in curs.description]

    def validate(self):
        "Check that our 2 tables have the same structure"
        # TODO: Change this to use Gerald
        # Do they have the same columns, in the same order?
        select_stmt = 'SELECT * FROM %s' % self.table_name
        source_curs = self.source_conn.cursor()
        source_curs.execute(select_stmt)
        source_cols = [col[0] for col in source_curs.description]
        target_curs = self.target_conn.cursor()
        target_curs.execute(select_stmt)
        target_cols = [col[0] for col in target_curs.description]
        if source_cols == target_cols:
            return 0
        else:
            return -1

    def dump_target_to_file(self, output_dir=None):
        "Dump the contents of this table in the target database to a csv file"
        if not hasattr(self, 'file_dir') and not output_dir:
            raise ValueError, "Cannot dump file without output directory"
        if output_dir:
            target_dir = output_dir
        else:
            target_dir = self.file_dir
        target_file = os.path.join(target_dir, self.table_name + '.csv')
        log.debug('Dumping %s to %s' % (self.table_name, target_file))
        csvDump.dump(self.target_conn, target_file, self.table_name)

    def dump_source_to_file(self, output_dir=None):
        "Dump the contents of this table in the source database to a csv file"
        if not hasattr(self, 'file_dir') and not output_dir:
            raise ValueError, "Cannot dump file without output directory"
        if output_dir:
            target_dir = output_dir
        else:
            target_dir = self.file_dir
        source_file = os.path.join(target_dir, self.table_name + '.csv')
        log.debug('Dumping %s to %s' % (self.table_name, source_file))
        csvDump.dump(self.source_conn, source_file, self.table_name)

    def truncate_target(self):
        "Truncate this table in the target database"
        curs = self.target_conn.cursor()
        curs.execute('truncate table %s' % self.table_name)

    def copy_source_to_target(self, batch_size=100):
        "Copy the contents of source to target"
        source_curs = self.source_conn.cursor()
        target_curs = self.target_conn.cursor()
        # Put together our column list for use in select and insert statements
        column_list = ','.join(self.columns)
        # Select from source - build statement
        selects = ['SELECT ', ]
        selects.append(column_list)
        selects.append(' FROM %s' % self.table_name)
        select_stmt = ''.join(selects)
        log.debug('copy: SELECT statement: %s' % select_stmt)
        # Select from source - get the data
        source_curs = self.source_conn.cursor()
        source_curs.execute(select_stmt)
        data_set = source_curs.fetchall() # Should stage data to a Tempfile
        log.info('copy: Source data extracted %d rows' % len(data_set))
        # Insert into target - build statement
        inserts = ['INSERT INTO %s ' % self.table_name]
        inserts.append('(')
        inserts.append(column_list)
        inserts.append(') VALUES (')
        column_clause = ','.join(('%s',) * len(self.columns))
        inserts.append(column_clause)
        inserts.append(')')
        insert_stmt = ''.join(inserts)
        log.debug('copy: INSERT statement: %s' % insert_stmt)
        # Insert into target - load the data
        target_curs = self.target_conn.cursor()
        row_count = 0
        for row in data_set:
            target_curs.execute(insert_stmt, row)
            row_count += 1
            if row_count % batch_size == 0:
                log.debug('copy: Committing at %d rows' % row_count)
                self.target_conn.commit()
        # On last commit to include the last few rows
        self.target_conn.commit()
        log.info('copy: Target loaded %d rows' % row_count)

def main(argv=None):
    """
    Main function modelled on Guido's guidelines
    """
    # Set defaults from db_refresh_config.py module (in this directory)
    SOURCE = None
    TARGET = None
    TABLES = None
    if os.path.isfile('db_refresh_config.py'):
        from db_refresh_config import SOURCE, TARGET, TABLES
    if argv is None:
        argv = sys.argv
    # parse command line options
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parser.add_argument("-s", "--source", help="URI for source database", default=SOURCE)
    parser.add_argument("-t", "--target", help="URI for target database", default=TARGET)
    parser.add_argument("-l", "--location", help="location of interim .csv files")
    parser.add_argument("-c", "--copy", help="Keep a copy of source data", action="store_true", default=False)
    args = parser.parse_args(argv[1:])
    # process options
    if args.debug:
        set_level(LOGNAME, 'DEBUG')
    else:
        set_level(LOGNAME, 'INFO')
    # Set location of interim files, default to current directory
    csv_dir = os.getcwd()
    if args.location:
        csv_dir = args.location
    log.debug('csv_dir set to %s' % csv_dir)
    # connect to source database
    if args.source:
        source_conn = dburi.get_connection(args.source)
    else:
        raise NameError, 'Must specify a source URI'
    log.debug('Connected to source - %s' % args.source)
    # connect to target
    if args.target:
        target_conn = dburi.get_connection(args.target)
    else:
        raise NameError, 'Must specify a target URI'
    log.debug('Connected to target - %s' % args.target)
    log.info("Started clearing out target db - %s" % args.target)
    table_list = []
    for table in TABLES:
        table_name = table['table_name']
        log.debug("Creating %s Table object" % table_name)
        cur_table = Table(table_name, source_conn, target_conn, csv_dir)
        table_list.append(cur_table)
        if args.copy:
            log.debug("Writing target data for %s to %s" % (table_name, csv_dir))
            cur_table.dump_target_to_file()
        log.debug("Truncating %s in target" % table_name)
        cur_table.truncate_target()
    log.info("Completed clearing out target db")
    # The copy is done in reverse order (reference tables first)
    rev_tables=table_list[:]
    rev_tables.reverse()
    for cur_table in rev_tables:
        table_name = cur_table.table_name
        log.debug("Loading %s data to target" % table_name)
        # Try and keep the contents in memory, may have to re-think this
        if args.copy:
            log.debug("Writing source data for %s to .csv file" % table_name)
            cur_table.dump_source_to_file()
        # TODO: If columns are defined only copy those
        cur_table.copy_source_to_target()
        log.debug("%s copied from source to target" % table_name)
    log.info("Completed copying data from source to target db")

if __name__ == "__main__":
    sys.exit(main())
