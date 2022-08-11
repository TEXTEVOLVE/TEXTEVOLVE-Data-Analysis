from collatex import *
import os
def dir_name(dir):
    return dir.name
cwd = os.getcwd()
#print("Current working directory: {0}".format(cwd))
#import contextlib
basedirectory = os.path.join(cwd, "Numbers Main")
with os.scandir(basedirectory) as folders:
    f=[folder for folder in folders if folder.is_dir()]
    f.sort(key=dir_name)
    for thisfolder in f:
        testdirectory=os.path.join(basedirectory, thisfolder.name)
        collation=Collation()
        with os.scandir(testdirectory) as texts:
            texts=[text for text in texts if not (text.name.endswith("DS_Store") or text.name.endswith("html"))]
            basetextpattern="EVR"
            basetext=[text for text in texts if basetextpattern in text.name][0]
            texts=[text for text in texts if not basetextpattern in text.name]
            texts.sort(key=dir_name)
            texts.insert(0, basetext)
            for text in texts:
                textfilepath=os.path.join(testdirectory, text)
                textcontents=open(textfilepath, encoding='utf-8').read()
                collation.add_plain_witness(text.name[:-4], textcontents)
        outputpath=os.path.join(testdirectory, thisfolder.name+".html")
        outfile = open(outputpath, 'w', encoding='utf-8')
        #with open(outputpath, 'w') as output:
        #with contextlib.redirect_stdout(output):
        alignment_table=collate(collation, layout='vertical', output='html2')
        print(alignment_table, file=outfile)
