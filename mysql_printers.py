#!/usr/bin/python

import gdb
import gdb.printing
import exceptions

def nice_str(v):
  if v == 0:
    return "NULL"
  else:
    inferior = gdb.selected_inferior()
    try:
      readable = inferior.read_memory(v, 1)
    except gdb.MemoryError:
      return "(invalid)"
    try:
      return v.string()
    except UnicodeDecodeError:
      return "(garbage)"

class MysqlPrinter(object):
  "Print a MYSQL structure"

  def __init__(self, val):
    self.val = val

  def to_string(self):
    return ("MYSQL connection to %s:%s as %s of db %s, "
            "with client status %s and server status %s" %
            (nice_str(self.val["host"]), self.val["port"], nice_str(self.val["user"]),
             nice_str(self.val["db"]), self.val["status"], self.val["server_status"]))

  def display_hint(self):
    return "array"

def mysql_lookup_function(val):
  lookup_tag = val.type.tag
  print "foo: %s" % lookup_tag
  if lookup_tag is None:
    return None

  if lookup_tag == "MYSQL":
    return MysqlPrinter(val)

def build_pretty_printer():
  print "registering types"
  pp = gdb.printing.RegexpCollectionPrettyPrinter("mysql_printers")
  pp.add_printer('MYSQL', r'st_mysql', MysqlPrinter)
  return pp
                                         
