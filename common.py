# Take string, return appropriate type
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

def merge_maps(m1, m2):
    if len(m1) != len(m2):
        print("Error: Length mismatch")
    l1 = []
    l2 = []
    for eb_id, a1 in m1.items():
        l1.append(a1)
        l2.append(m2[eb_id])
    return l1, l2

