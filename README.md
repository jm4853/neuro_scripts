# Neuro Scripts
## TODO
- [ ] Investigate why there is a 0 EBrains ID in map file but not in 1000Brains dataset
- [ ] Add statistical analysis
- [ ] Add visualization

## Environment
To use `neuro_help.py`, the environment variable `CS455_HCP_DATA_ROOT` must be set before importing. This should point to the `HCP_ebrains` directory, which should contain `demographics` and `ebrains_strFunc_200subj` directories. To use `bct_help.py`, the environment variable `CS455_BCT_DATA_ROOT` must be set before importing. This should point to the `bctWrapper` directory, which should contain `features` and `src` directories.


## Basic Usage
```python
from neuro_help import data
from common import merge_maps
row = 4
col = 5
e = data.get_edge_map(row, col, connectome="fc")
a = data.get_attribute_map("Age")
edges, ages = merge_maps(e, a)
```
```python
from neuro_help import data
from common import merge_maps
from bct_help import bdata
node_idx = 7
eb_ids = data.get_eb_ids()
f = bdata.get_feature_map("node_betweenness_centrality", node_idx, eb_ids)
a = data.get_attribute_map("Age")
del a[0]    # Must remove 0 ID for now (see TODO)
features, ages = merge_maps(f, a)
```
