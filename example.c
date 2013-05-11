#include <mysql/mysql.h>
#include <stddef.h>
#include <stdio.h>

void err(MYSQL* mysql, int result) {
  if (result != 0) {
    printf("error: %d -> %s\n", mysql_errno(mysql), mysql_error(mysql));
  }
}

int main() {
  MYSQL mysql;
  mysql_init(&mysql);
  mysql_options(&mysql, MYSQL_READ_DEFAULT_GROUP, "client");
  if (!mysql_real_connect(&mysql, "localhost", NULL, NULL, NULL, 3306, NULL, 0)) {
    err(&mysql, 1);
  }
  int result = mysql_query(&mysql, "SHOW STATUS");
  err(&mysql, result);
  MYSQL_RES* res = mysql_store_result(&mysql);
  return 0;
}
