import os, sys
import re
import nltk

def load_description(fname):
    with open(fname) as fp:
        data = fp.read().decode('ascii', 'ignore')
    data = data.replace("\n", " ")
    res = re.findall("Description:.*?<p>(.*?)</div>", data)
    if len(res) == 0: return ""
    try: assert len(res) == 1
    except:
        print res
        raise
    res = res[0]
    res = re.sub("<.*?>", "", res)
    return res

def main():
    with open("common-english-words.txt") as fp:
        common_words = set(fp.read().strip().split(","))
    words = []
    for i, fname in enumerate(os.listdir("./Watsi_data_downloaded/")):
        if not ( fname.startswith("profile") or fname.endswith(".html") ): continue
        desc = load_description(os.path.join("./Watsi_data_downloaded/", fname))
        for sentence in nltk.sent_tokenize(desc):
            for word in nltk.word_tokenize(sentence):
                word = word.lower()
                if word.isdigit(): continue
                if word in ".,;?'\":-+!()[]%$": continue
                if word.startswith("\\"): continue
                if word in common_words: continue
                words.append(word)
    for word in words:
        print word
    
if __name__ == '__main__':
    main()
