import re
string = """
Это курс информатики соответствует ФГОС и ПООП, это подтверждено ФГУ ФНЦ 
НИИСИ РАН
"""
def text_handler(text):
 regex = r"[А-Я]{2,}(?:[\s]*[А-Я]{2,})*"
 matches = re.findall(regex, text)
 return matches

def text_compare(string1, string2):
 substring = string2.split("*", 2)[0]
 if string1.startswith(substring):
  print("OK")
 else:
  print("KO")

def input_strings():
 a = input("enter first word: ")
 b = input("enter second word: ")
 text_compare(a, b)


#print(text_handler(string))
input_strings()
