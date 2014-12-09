#!/usr/bin/env python

'''simple starter for the moxy program - used by developers'''

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join('src')))
from moxy import main
main.main()
