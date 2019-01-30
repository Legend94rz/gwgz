import re
import os
import shutil

if __name__=="__main__":
    with open(r"F:\Workshop\古文觀止\material\古文觀止_fulltext.md", 'r', encoding='utf8') as fin:
        lines = fin.readlines()

    title = []
    lnum = []
    for i in range(len(lines)):
        f = re.match('^卷(.*)·(.*)\t(.*)$', lines[i])
        if f:
            title.append(lines[i])
            lnum.append(i)

    lnum.append(len(lines))
    for i in range(len(title)):
        f = re.match('^卷(.*)·(.*)\t(.*)$', title[i])
        os.makedirs( 'F:/Workshop/古文觀止/material/卷之%s' % f.group(1), exist_ok=True )
        with open('F:/Workshop/古文觀止/material/卷之%s/%d-%s-%s.md'%(f.group(1).strip(), i+1, f.group(2).strip(), f.group(3).strip()), 'w', encoding='utf8') as fout:
            fout.writelines(lines[lnum[i]+2 : lnum[i+1]])
