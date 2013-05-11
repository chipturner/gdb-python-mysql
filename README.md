gdb-python-mysql
================

GDB Pretty Printers for MySQL data structures

Work in progress.

How to use:

Put this in your .gdbinit:

    python
    sys.path.insert(0, '/path/to/gdb-python-mysql')

    import gdb.printing
    import mysql_printers
    gdb.printing.register_pretty_printer(
        gdb.current_objfile(),
        mysql_printers.build_pretty_printer())
    end