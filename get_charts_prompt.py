import os
import glob
import re

os.chdir('model8/original_data')

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


def get_files():
    files = [file for file in glob.glob("*.txt")]
    #files=['Number_of_top_Unis.txt']
    print(files)
    return files


def get_first_sentences(files):
    all_files = {}

    for file in files:
        first_sentences = []
        with open(file, 'r', encoding='latin1') as f:
            data = f.read()
            descriptions = data.split('"')
            descriptions = [i for i in descriptions if (i != '\n') and (i != '\n\n\n') and (i != '\n\n\n\n')]
            print(descriptions[:10],'\n')
            for desc_idx in range(0,len(descriptions)):
                sentence = descriptions[desc_idx].split('.')
                first_sent = sentence[0]
                first_sent = cleanhtml(first_sent)
                first_sent = re.sub(r"\s+", " ", first_sent)
                #print('first_sent=',first_sent,'\n')
                first_sentences.append(first_sent)
        all_files[file] = first_sentences
    #print(all_files)

    '''print(len(first_sentences))
    with open('output.txt', 'w', encoding='latin1') as g:
        for sent in first_sentences:
            g.write(sent)
    g.close()'''


if __name__ == '__main__':
    files = get_files()
    get_first_sentences(files)