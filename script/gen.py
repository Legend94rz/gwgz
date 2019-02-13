import argparse
import sys
import re
import os

column = ["卷之一","卷之二","卷之三","卷之四","卷之五","卷之六","卷之七","卷之八","卷之九","卷之十","卷之十一","卷之十二"]

class FootnoteNumbers():
    def __init__(self, start = 1, prefix = '1.', type = 'in_text'):
        self.no = start
        self.prefix = prefix
        self.type=type

    def get_sub(self, match, type=None):
        t = type
        if t is None:
            t=self.type
        if t=='in_text':
            return f'<a id="{self.prefix}{self.no}" href="#fn{self.prefix}{self.no}"><sup>[{self.no}]</sup></a>'
        elif t=='in_notation':
            return f'<p><a id="fn{self.prefix}{self.no}" href="#{self.prefix}{self.no}">[{self.no}]</a> {match.group(1)} </p>'
        elif t=='in_text_end':
            return f'<a id="{self.prefix}{self.no}" href="#fn{self.prefix}{self.no}"><sup></sup></a>\n\n'
        elif t=='in_notaion_end':
            return f'<p><a id="fn{self.prefix}{self.no}" href="#{self.prefix}{self.no}"> </a> </p>\n\n'

    def __call__(self, match):
        s = self.get_sub(match)
        self.no+=1
        return s

def parse_args(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="My Python script.")
    parser.add_argument("-n", "--number", type=int, default=3, help="Total number of text.")
    return parser.parse_args(argv)

def origin(no, lines):
    out = ''
    for i in range(len(lines)-1):
        if len(lines[i+1].strip())>0 and lines[i].endswith('\n') and len(lines[i].strip())>0:
            out+=lines[i].rstrip('\n')
        else:
            out+=lines[i]
    out+=lines[-1]
    fn = FootnoteNumbers(1, f'{no}.', 'in_text')
    out = re.sub('\[\]', fn, out)
    out+= fn.get_sub(match=None, type='in_text_end')
    return fn.no, out

def notation(no, lines):
    out = ''.join(lines)
    fn =  FootnoteNumbers(1, f'{no}.', 'in_notation')
    out = re.sub('\[\] (.*)', fn, out)
    out+=fn.get_sub(match=None, type='in_notaion_end')
    return fn.no, out

def remark(lines):
    return ''.join(lines)

def translation(lines):
    out = ''
    for i in range(len(lines)-1):
        if len(lines[i+1].strip())>0 and lines[i].endswith('\n') and len(lines[i].strip())>0:
            out+=lines[i].rstrip('\n')
        else:
            out+=lines[i]
    out+=lines[-1]
    return out

def one_text(folder, file):
    hd = ['#### 正文\n', '#### 注釋\n', '#### 評注\n', '#### 譯文\n']
    id = []
    with open(os.path.join(folder, file), 'r', encoding='utf8') as fin:
        lines=fin.readlines()
    for i in range(len(lines)):
        if lines[i]==hd[len(id)]:
            id.append(i)
            if len(id)==len(hd):break
    s = file.rstrip('.md').split('-')
    print(file)
    title = '### %s\t%s\n' % (s[1], s[2])
    no1, text = origin(s[0], lines[id[0]: id[1]])
    no2, nota = notation(s[0], lines[id[1]: id[2]])
    assert(no1==no2)
    rema = remark(lines[id[2]: id[3]])
    tran = translation(lines[id[3]:])
    return title + text+nota+rema+tran

def sort_file(fd):
    lst = os.listdir(fd)
    return sorted(lst, key=lambda x: int(x.rstrip('.md').split('-')[0]))


if __name__=="__main__":
    args = parse_args()
    book_name = '# 古文觀止\n\n'
    content = ''
    texts = []
    for col in column:
        each_col = f'## 古文觀止 {col}\n'
        for fn in sort_file(f'../material/{col}'):
            p = fn.split('-')
            if int(p[0])>args.number:
                break
            txt = one_text(f'../material/{col}', fn)
            each_col+=txt
        texts.append(each_col)

    full_text = open('../material/full_text.md','w',encoding = 'utf8')
    full_text.write(book_name)
    full_text.write(content)
    full_text.writelines(texts)
    full_text.close()