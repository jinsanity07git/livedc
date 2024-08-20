# livedc
 useful mathmatical models/caculators for daily life and cloud deployment

tdm23_vr setup for colab
```shell
!pip install livedc
from livedc import url_vrpkl,url_vrlib
import pickle
with open(url_vrpkl, "rb") as f:
    prereq = pickle.load(f)
tdmvr, installed_packages = prereq.env(furl=url_vrlib)
```