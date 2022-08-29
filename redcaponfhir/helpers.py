def clean_empty(d):
    if isinstance(d, dict):
        return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}
    if isinstance(d, list):
        return [v for v in map(clean_empty, d) if v]
    return d
