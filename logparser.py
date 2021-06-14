import sys
import csv
import re
import operator

num_error_msg = {}
entries_per_usr = {}

with open("syslog.log", 'r') as f:
  lines = f.readlines()
  for line in lines:
    pattern1 = r"(INFO)"
    pattern2 = r"(ERROR)"

    user_pattern = r"\(([a-z.]+)\)"

    if re.search(pattern1, line):
      user = re.search(user_pattern, line).groups()[0]

      if user not in entries_per_usr:
        entries_per_usr[user] = [1, 0]
      else:
        entries_per_usr[user][0] += 1

    elif re.search(pattern2, line):
      err = re.search(r"ERROR ([a-zA-Z ']+) ", line).groups()[0]
      user = re.search(user_pattern, line).groups()[0]
      if err not in num_error_msg:
        num_error_msg[err] = 1
      else:
        num_error_msg[err] += 1

      if user not in entries_per_usr:
        entries_per_usr[user] = [0, 1]
      else:
        entries_per_usr[user][1] += 1

f.close()

with open('csv_file.csv', 'w') as csvfile:
  csv_columns = ['error', 'number']
  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
  writer.writeheader()
  for data in num_error_msg.items():
      csvfile.write("{}, {}\n".format(data[0], data[1]))
csvfile.close()

with open('csv_file2.csv', 'w') as csvfile:
  csv_columns = ['user','info','error']
  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
  writer.writeheader()
  for data in entries_per_usr.items():
    csvfile.write("{}, {}, {}\n".format(data[0], data[1][0], data[1][1]))
csvfile.close()