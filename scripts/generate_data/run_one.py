import sys, importlib
sys.path.insert(0, __file__.rsplit('/',1)[0])
m = importlib.import_module(sys.argv[1]); meta = m.run()
for t in meta['tables']: print(t['name'], t['rowCount'])
