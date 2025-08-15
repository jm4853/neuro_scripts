from pathlib import Path
import os

DATA_ROOT=Path(os.environ.get("CS455_DATA_ROOT", "/mnt/c/Users/Jake/Documents/cs455/project/data/HCP_ebrains"))
SC_DIR = DATA_ROOT / "ebrains_strFunc_200subj/connectomes/Schaefer100/1StructuralConnectivity"
FC_DIR = DATA_ROOT / "ebrains_strFunc_200subj/connectomes/Schaefer100/2FunctionalConnectivity"
DEMO_DIR = DATA_ROOT / "demographics"
ID_DIR = DATA_ROOT / "ebrains_strFunc_200subj/demographics/src"

# Note: DEMO_DIR / "HCP_S1200_DataDictionary_April_20_2018.xlsx" contains descriptions of each measure
# Note: Generally, everything uses ebrains IDs

class Data:
    def __init__(self):
        self.eb_to_hcp = dict()
        self.hcp_to_eb = dict()
        self.subjects = dict()
        self.attributes = []

    def add_subject(self, s):
        if s.hcp_id == None:
            s.hcp_id = self.eb_to_hcp.get(s.eb_id, None)
        self.subjects[s.eb_id] = s

    def get_subject(self, eb_id):
        eb_id = int(eb_id)
        if not eb_id in self.subjects.keys():
            # Maybe hcp_id was passed in instead of eb_id
            eb_id = self.hcp_to_eb[eb_id]
        return self.subjects.get(eb_id, None)

    def drop_subject(self, eb_id):
        eb_id = int(eb_id)
        if not eb_id in self.subjects.keys():
            # Maybe hcp_id was passed in instead of eb_id
            eb_id = self.hcp_to_eb[eb_id]
        if eb_id in self.subjects.keys():
            del self.subjects[eb_id]

    def get_attribute_map(self, attribute):
        if not attribute in self.attributes:
            print(f"Error: Invalid attribute: \"{attribute}\"")
            return None
        attr_map = dict()
        for eb_id, s in self.subjects.items():
            attr_map[eb_id] = s.attrs.get(attribute, None)
        return attr_map

    def get_edge_map(self, edge_i, edge_j, connectome="sc"):
        edge_map = dict()
        if connectome.lower() == "sc":
            edge_map = {eb_id: s.sc[edge_i][edge_j] for eb_id, s in self.subjects.items()}
        elif connectome.lower() == "fc":
            edge_map = {eb_id: s.fc[edge_i][edge_j] for eb_id, s in self.subjects.items()}
        else:
            print(f"Error: Invalid connectome type \"{connectome}\"")
            return None
        return edge_map
        


class Subject:
    def __init__(self, eb_id, hcp_id=None):
        self.eb_id = int(eb_id)
        self.hcp_id = hcp_id
        self.sc = [[]]
        self.fc = [[]]
        self.attrs = None

    def set_attributes(self, d):
        self.attrs = d

data = Data()


def populate_id_maps():
    global data
    with open(ID_DIR / "SubjectConversion_EBRAINS.txt", "r") as f:
        ebrain_ids = f.readlines()[1:]  # First line is a comment
    with open(ID_DIR / "1GeneralCode_SubjectIDList.txt", "r") as f:
        hcp_ids = f.readlines()
    if len(ebrain_ids) != len(hcp_ids):
        print(f"Error: Length mismatch")
        return
    data.eb_to_hcp = {int(k): int(v) for k, v in zip(ebrain_ids, hcp_ids)}
    data.hcp_to_eb = {int(k): int(v) for k, v in zip(hcp_ids, ebrain_ids)}


def populate_subject_connectomes(s):
    eb_id = int(s.eb_id)
    with open(SC_DIR / f"{eb_id:03}/Counts.csv", "r") as f:
        sc = [[int(v) for v in l.split() if v] for l in f.readlines()]
    with open(FC_DIR / f"{eb_id:03}/EmpCorrFC_concatenated.csv", "r") as f:
        fc = [[float(v) for v in l.split() if v] for l in f.readlines()]
    s.sc = sc
    s.fc = fc

def handle_type(s):
    s = s.strip()
    try:
        if len(s) == 0:
            return None
        if s.isdigit():
            return int(s)
        else:
            return float(s)
    except ValueError:
        return s

def populate_demographics():
    if not (data.eb_to_hcp and data.hcp_to_eb):
        populate_id_maps()
    if not data.subjects:
        populate_connectomes()
    with open(DEMO_DIR / "hcp_1200demographics.csv", "r") as f:
        keys = f.readline().split(",")
        for l in f.readlines():
            d = {k.strip(): handle_type(v) for k, v in zip(keys, l.split(","))}
            hcp_id = d["Subject"]
            del d["Subject"]
            eb_id = data.hcp_to_eb.get(hcp_id, None)
            if eb_id != None:
                if eb_id in data.subjects.keys():
                    data.subjects[eb_id].set_attributes(d)
                else:
                    print("Error: ID not in mapping")
        data.attributes = keys[1:] # Everything except "Subject"
        

def populate_connectomes():
    if not (data.eb_to_hcp and data.hcp_to_eb):
        populate_id_maps()
    for eb_id in data.eb_to_hcp.keys():
        s = Subject(eb_id, hcp_id=data.eb_to_hcp.get(eb_id, None))
        populate_subject_connectomes(s)
        data.add_subject(s)

def merge_maps(m1, m2):
    if len(m1) != len(m2):
        print("Error: Length mismatch")
    l1 = []
    l2 = []
    for eb_id, a1 in m1.items():
        l1.append(a1)
        l2.append(m2[eb_id])
    return l1, l2





populate_demographics()
