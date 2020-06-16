import io
import json

a_file = io.open('tweets.txt','r',encoding='utf-8')
string_without_line_breaks = ""
for line in a_file:
  stripped_line = line.rstrip()
  string_without_line_breaks += stripped_line
a_file.close()

b_file = io.open('tweets2.txt','a',encoding='utf-8')
b_file.write(string_without_line_breaks)
b_file.close()