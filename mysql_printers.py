#!/usr/bin/python

import gdb
import gdb.printing
import exceptions

def nice_str(v, length=None):
  if v == 0:
    return "NULL"
  else:
    inferior = gdb.selected_inferior()
    try:
      readable = inferior.read_memory(v, 1)
    except gdb.MemoryError:
      return "(invalid)"
    try:
      if length is not None:
        return '"%s"' % v.string(length=length)
      else:
        return '"%s"' % v.string()
    except UnicodeDecodeError:
      return "(garbage)"

class MysqlPrinter(object):
  "Print a MYSQL structure"

  def __init__(self, val):
    self.val = val

  def to_string(self):
    return ("MYSQL connection to %s:%s as %s of db %s, "
            "with client status %s and server status %s" %
            (nice_str(self.val["host"]),
             self.val["port"],
             nice_str(self.val["user"]),
             nice_str(self.val["db"]),
             self.val["status"],
             self.val["server_status"]))

  def display_hint(self):
    return "array"

class MysqlResultPrinter(object):
  def __init__(self, val):
    self.val = val

  def to_string(self):
    fields = []
    for i in range(int(self.val["data"]["fields"])):
      fields.append(self.val["fields"][i])

    row = self.val["data"]["data"]
    cursor_idx = 0
    while row and row["data"] != self.val["current_row"]:
        cursor_idx += 1
        row = row["next"]
    if not row:
        cursor_idx = "(invalid cursor)"

    if self.val["handle"]:
        fetch_type = "use_results"
    else:
        fetch_type = "store_results"

    return ("MYSQ_RES of %d rows, type %s, eof %s; cursor is at row %s; "
            "fields = { %s }" %
            (self.val["row_count"], fetch_type, bool(self.val["eof"]),
             cursor_idx, ", ".join(str(f) for f in fields)))

  def display_hint(self):
    return "array"

  def children(self):
    return self._result_iterator(self.val)

  class _result_iterator(object):
    def __init__(self, val):
      self.val = val
      self.current_row = self.val["data"]["data"]
      self.row_count = int(self.val["data"]["rows"])
      self.field_count = int(self.val["data"]["fields"])
      self.row_number = 0

    def __iter__(self):
      return self

    def next(self):
      if self.current_row is None:
        raise StopIteration

      row = self.current_row
      self.current_row = self.current_row["next"]
      self.row_number += 1
      return ("[%d]" % (self.row_number - 1),
              "(%s)" % ",".join(nice_str(row["data"][idx], row["data"][idx + 1] - row["data"][idx] - 1)
                                for idx in range(self.field_count)))

class MysqlFieldPrinter(object):
  def __init__(self, val):
    self.val = val

  def to_string(self):
    return ("MYSQL_FIELD(%s, type %d)" % (nice_str(self.val["name"]), self.val["type"]))

  def display_hint(self):
    return "array"



def build_pretty_printer():
  pp = gdb.printing.RegexpCollectionPrettyPrinter("mysql_printers")
  pp.add_printer('MYSQL', r'^st_mysql$', MysqlPrinter)
  pp.add_printer('MYSQL_RES', r'^st_mysql_res$', MysqlResultPrinter)
  pp.add_printer('MYSQL_FIELD', r'^st_mysql_field$', MysqlFieldPrinter)
  return pp
                                         
