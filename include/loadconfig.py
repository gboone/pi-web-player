from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def loadconfig(config=""):
    yamlFile=open(config, "r", encoding="utf-8")
    return load(yamlFile, Loader)
