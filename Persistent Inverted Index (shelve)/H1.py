import shelve
from collections import defaultdict
import os,glob


special_characters = ['!','"','#','$','%','&','(',')','*','+','/',':',';','<','=','>','@','[','\\',']','^','`','{','|','}','~','\t','.',',']
folder_path = './txt'
dic = defaultdict(set)

# for filename in glob.glob(os.path.join(folder_path, '*.txt')):
#     with open(filename, 'r', encoding="utf8") as f:
#         text = f.read()
#         for i in special_characters: 
#             text = text.replace(i, '')
#         text = text.lower()

#         for x in text.split(" "):
#             dic[x].add(str(filename).replace("./txt\\",""))






# s = shelve.open('persistency/dict')
# try:
#     s.update(dic)
# finally:
#     s.close()


s = shelve.open('./persistency/dict')
#print(s['operate'])
print(s["kill"] & s["horse"])

""" 
print()
print(s["kill"] & s["kiss"])
print()
print(s["love"] & s["kiss"])
print()
print(s["kill"] & s["love"])
print()
print(s["gun"] | s["david"]) """