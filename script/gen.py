import argparse
import sys
import re


def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="My Python script.")
    return parser.parse_args(argv)

def origin(lines):
    out = ''
    for i in range(len(lines)-1):
        if not lines[i+1].startswith(' ') and lines[i].endswith('\n'):
            out+=lines[i].rstrip('\n')
        else:
            out+=lines[i]
    out+=lines[-1]
    return out

def notation(lines):
    pass

def translation(lines):
    pass

def remark(lines):
    pass

if __name__=="__main__":
    rep = {}
    with open(r"F:\Workshop\古文觀止\material\oov.txt", encoding='utf8') as fin:
        for row in fin:
            r=row.split()
            if len(r)==2:
                rep[r[0]] = r[1]

    with open(r"F:\Workshop\古文觀止\material\卷之一周文\鄭伯克段于鄢.md", encoding='utf8') as fin:
        all = fin.readlines()
    
    splits = []
    for i in range(len(all)):
        if all[i]=='$\n':
            splits.append(i)
    ori_txt = origin(all[:splits[0]])
    not_txt = notation(all[splits[0]+1: splits[1]])
    tra_txt = translation(all[splits[1]+1: splits[2]])
    rem_txt = remark(all[splits[2]+1: ])
    
