import difflib
import os
os.getcwd()
cwd = os.getcwd()
print("Current working directory: {0}".format(cwd))
#import contextlib
basedirectory = os.path.join(cwd, "Numbers Main")
with os.scandir(basedirectory) as folders:
    folders=[folder for folder in folders if folder.is_dir()]
    for folder in folders:
        print(folder)
        testdirectory=os.path.join(basedirectory, folder)
        with os.scandir(testdirectory) as texts:
            texts=[text for text in texts if not (text.name.endswith("DS_Store") or text.name.endswith("html"))]
            basetextpattern="EVR"
            basetext=[text for text in texts if basetextpattern in text.name][0]
            basetextfilepath=os.path.join(testdirectory, basetext)
            basetextcontents=open(basetextfilepath, encoding='utf-8').read()
            texts=[text for text in texts if not basetextpattern in text.name]
            for text in texts:
                print(text)
                textfilepath=os.path.join(testdirectory, text)
                textcontents=open(textfilepath, encoding='utf-8').read()
                textcontents.split()
                print(textcontents.split())
                difference = difflib.HtmlDiff(tabsize=2)
                s=difflib.SequenceMatcher()
                s.set_seqs(basetextcontents.split(), textcontents.split())
                ratio=s.ratio()
                outputpath=os.path.join(testdirectory, folder.name+"_"+text.name[:-4]+".html")
                with open(outputpath, "w") as fp:
                    html = difference.make_file(fromlines=basetextcontents.split(), tolines=textcontents.split(), fromdesc=basetext.name[:-4], todesc=text.name[:-4])
                    fp.write(html)
                    fp.write("Similarity Ratio: %f" %(ratio))
