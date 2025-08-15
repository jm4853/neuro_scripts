# Neuro Scripts
## `CS455_DATA_ROOT`
The environment variable `CS455_DATA_ROOT` must be set before importing any code. This should point to the "HCP\_ebrains" directory, which should contain "demographics" and "ebrains\_strFunc\_200subj" directories.


## Basic Usage
```python
from neuro_help import *
row = 4
col = 5
e = data.get_edge_map(row, col, connectome="fc")
a = data.get_attribute_map("Age")
edges, ages = merge_maps(e, a)
```
