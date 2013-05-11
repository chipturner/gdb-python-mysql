#!/usr/bin/python

import gdb
import gdb.printing

class MysqlPrinter(object):
  "Print a MYSQL structure"

  def __init__(self, val):
    self.val = val

  def to_string(self):
    return "MYSQL connection <%s:%s as %s to %s>" % (self.val["host"], self.val["port"], self.val["user"], self.val["db"])

  def display_hint(self):
    return "string"

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
                                         
