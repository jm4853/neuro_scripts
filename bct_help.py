from pathlib import Path
import os
from common import handle_type

BCT_FEATURES_DIR = None
BCT_SUBJECT_LIST = None

try:
    BCT_DATA_ROOT = Path(os.environ["CS455_BCT_DATA_ROOT"])
except KeyError:
    BCT_DATA_ROOT = None
    print("Warning: CS455_BCT_DATA_ROOT not set, cannot use graph theory measures")

if BCT_DATA_ROOT:
    BCT_FEATURES_DIR = BCT_DATA_ROOT / "features"
    BCT_SUBJECT_LIST = BCT_DATA_ROOT / "src/subjects.txt"


class bctData:
    def __init__(self):
        self.subjects = None
        self.features = dict()

    def set_subjects(self, s):
        self.subjects = s

    def set_features(self, f):
        self.features = f

    def get_feature_map(self, feature, node_idx=None, eb_id_subset=None):
        if not feature in self.features.keys():
            print(f"Error: Invalid feature \"{feature}\"")
            return None
        ids = eb_id_subset
        if not ids:
            ids = list(set([eb_id for eb_id, _ in self.subjects]))
        f = dict()
        for eb_id in ids:
            if not eb_id:
                continue
            y = self.features[feature][eb_id].get(1, None)
            if node_idx != None:
                f[eb_id] = y[node_idx]
            else:
                f[eb_id] = y
        return f

bdata = bctData()

def load_subjects():
    subjects = []
    with open(BCT_SUBJECT_LIST, "r") as f:
        for l in f.readlines():
            eb_id = int(l[:4])
            scan_n = int(l[5:6])
            subjects.append((eb_id, scan_n))
    bdata.set_subjects(subjects)

def load_features():
    features = dict()
    for filename in os.listdir(BCT_FEATURES_DIR):
        p = Path(f"{BCT_FEATURES_DIR}/{filename}")
        if p.suffix == ".txt":
            with open(p, "r") as f:
                f_d = dict()
                for i, l in enumerate(f.readlines()):
                    eb_id, scan_n = bdata.subjects[i]
                    l = l.strip()
                    if len(l.split()) == 1:
                        v = handle_type(l)
                    else:
                        v = [handle_type(x) for x in l.split()]
                    if not eb_id in f_d.keys():
                        f_d[eb_id] = dict()
                    f_d[eb_id][scan_n] = v
                features[p.stem] = f_d
    bdata.set_features(features)



load_subjects()
load_features()
