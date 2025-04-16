# from .desc import add_rdoc
import os

prefix = os.path.dirname(__file__)
url_vrpkl = os.path.join( prefix,  'vr/tdm23.vr.pkl') 
url_vrlib   = os.path.join( prefix,  'vr/tdm23.vr') 
"""
!pip install livedc
from livedc import url_vrpkl,url_vrlib
import pickle
with open(url_vrpkl, "rb") as f:
    prereq = pickle.load(f)
tdmvr, installed_packages = prereq.env(furl=url_vrlib)
"""

"""
python -c "import livedc"
"""

__version__ = "0.0.17"