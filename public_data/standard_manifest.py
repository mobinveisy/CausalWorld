"""Canonical manifest contract used by CausalWorld public-dataset experiments."""
REQUIRED_COLUMNS = [
    'dataset','trial_id','split','property_name','property_value',
    'context_group','pair_id','state_path','source_path'
]

def validate(df):
    missing=[c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing: raise ValueError(f'Missing columns: {missing}')
    return True
