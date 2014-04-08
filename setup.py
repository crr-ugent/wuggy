import sys
import os
from setuptools import setup, find_packages

from distutils.core import setup
from esky import bdist_esky

import info


if sys.platform in ['win32','cygwin','win64']:
    freezer_module="py2exe"
    freezer_options= {'argv_emulation': False,
                      'windows':['Wuggy.py']}
    # ICON="./icons/wug.ico"

    
elif sys.platform == 'darwin':
    freezer_module="py2app"
    freezer_options= {'argv_emulation': False,
                      'iconfile': 'icons/wug.icns',
                      'plist': {"CFBundleShortVersionString": info.Version,
                      "CFBundleVersion": info.Build,
                      "NSHumanReadableCopyright": info.Copyright,
                      "Bundle identifier":  info.Identifier}}
    # ICON="./icons/wug.icns"

lexica=['orthographic_basque.txt', 'orthographic_dutch.txt', 
        'orthographic_english.txt', 'orthographic_french.txt', 
        'orthographic_german.txt', 'orthographic_italian.txt',
        'orthographic_polish.txt', 'orthographic_serbian_cyrillic.txt',
        'orthographic_serbian_latin.txt', 'orthographic_spanish.txt',
        'orthographic_vietnamese.txt', 'phonetic_english_celex.txt',
        'phonetic_english_cmu.txt', 'phonetic_french.txt',
        'phonetic_italian.txt']
        
lexica_paths=['data/'+lexicon for lexicon in lexica]

plugins=['__init__.py', 'base_plugin.py', 'orthographic_basque.py', 'orthographic_dutch.py', 'orthographic_english.py', 'orthographic_french.py', 'orthographic_german.py', 'orthographic_italian.py', 'orthographic_polish.py', 'orthographic_serbian.py', 'orthographic_serbian_cyrillic.py', 'orthographic_serbian_latin.py', 'orthographic_spanish.py', 'orthographic_vietnamese.py', 'phonetic_english_celex.py', 'phonetic_english_cmu.py', 'phonetic_french.py', 'phonetic_italian.py', 'segment.py', 'subsyllabic_common.py']

plugins_paths=['plugins/'+ plugin for plugin in plugins]

orth_plugins=['__init__.py', 'de.py', 'en.py', 'es.py', 'fr.py', 'it.py', 'nl.py', 'pl.py', 'sr_cyrillic.py', 'sr_latin.py', 'vi.py']

orth_plugins_paths=['plugins/orth/'+ orth_plugin for orth_plugin in orth_plugins]

phon_plugins=['__init__.py', 'fr.py', 'it.py']

phon_plugins_paths=['plugins/phon/'+ phon_plugin for phon_plugin in phon_plugins]


Wuggy_executable = bdist_esky.Executable(
    gui_only = True,
    description = "A multilingual pseudoword generator",
    script = "Wuggy.py")

setup(name=info.Name,
      version=info.Version,
      scripts=[Wuggy_executable],
      packages=find_packages(),
      data_files=[('data', lexica_paths),
                  ('plugins', plugins_paths),
                  ('plugins/orth', orth_plugins_paths),
                  ('plugins/phon', phon_plugins_paths)],
      options={
      'bdist_esky':{"freezer_module":freezer_module,
                    "freezer_options": freezer_options,
                    "includes": ["Levenshtein"],
                    "excludes": ["plugins"],}
      })
