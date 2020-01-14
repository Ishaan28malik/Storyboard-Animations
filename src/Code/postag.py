import os
import re
from nltk.tag.stanford import StanfordPOSTagger
from nltk import word_tokenize
import json
import helpers

if not os.path.exists('scenes'):
  print('Scenes folder doesn\'t exist :( Run prepare.py first', end='\n')

pos_tagger = StanfordPOSTagger(r'english-bidirectional-distsim.tagger')

for filename in sorted(os.listdir('scenes'), key=helpers.natural_keys):
  scenefile = open('scenes/' + filename, 'r+')
  scene = json.load(scenefile)
  scene['processed'] = list()
  for sentence in scene['raw']:
    words = word_tokenize(sentence)
    words = list(filter(None, [re.sub(r'\W+', '', word) for word in words]))
    scene['processed'].append(words)
  scene['processed'] = pos_tagger.tag_sents(scene['processed'])
  scenefile.seek(0)
  json.dump(scene, scenefile, indent=2)
  scenefile.truncate()
  scenefile.close()
