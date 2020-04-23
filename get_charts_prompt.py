import os
import glob
import re

os.chdir('model8/original_data')

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

files = [file for file in glob.glob("*.txt")]
files=['Number_of_top_Unis.txt']
print(files)

first_sentences = []

for file in files:
    with open(file, 'r', encoding='latin1') as f:
        data = f.read()
        descriptions = data.split('\"')
        descriptions = [i for i in descriptions if (i != '\n') and (i != '\n\n\n') and (i != '\n\n\n\n')]
        print(descriptions[:10],'\n')
        for desc_idx in range(0,len(descriptions)):
            sentence = descriptions[desc_idx].split('.')
            first_sentences.append(cleanhtml(sentence[0]))

print(len(first_sentences))
with open('output.txt', 'w', encoding='latin1') as g:
    for sent in first_sentences:
        g.write(sent+'\n')
g.close()