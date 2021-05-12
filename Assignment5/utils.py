# membership functions for angle θ
theta_ranges = {
    'NVB': (None, -25, -40),
    'NB': (-40, -10),
    'N': (-20, 0),
    'ZO': (-5, 5),
    'P': (0, 20),
    'PB': (10, 40),
    'PVB': (25, None, 40)
}

# membership functions for angular speed ω
omega_ranges = {
    'NB': (None, -3, -8),
    'N': (-6, 0),
    'ZO': (-1, 1),
    'P': (0, 6),
    'PB': (3, None, 8)
}

# membership functions for traction force F
f_ranges = {
    'NVVB': (None, -24, -32),
    'NVB': (-32, -16),
    'NB': (-24, -8),
    'N': (-16, 0),
    'Z': (-4, 4),
    'P': (0, 16),
    'PB': (8, 24),
    'PVB': (16, 32),
    'PVVB': (24, None, 32)
}

# rules for the fuzzy system
fuzzy_rules = {
    'PVB': {'NB': 'P', 'N': 'PB', 'ZO': 'PVB', 'P': 'PVVB', 'PB': 'PVVB'},
    'PB': {'NB': 'Z', 'N': 'P', 'ZO': 'PB', 'P': 'PVB', 'PB': 'PVVB'},
    'P': {'NB': 'N', 'N': 'Z', 'ZO': 'P', 'P': 'PB', 'PB': 'PVB'},
    'ZO': {'NB': 'NB', 'N': 'N', 'ZO': 'Z', 'P': 'P', 'PB': 'PB'},
    'N': {'NB': 'NVB', 'N': 'NB', 'ZO': 'N', 'P': 'Z', 'PB': 'P'},
    'NB': {'NB': 'NVVB', 'N': 'NVB', 'ZO': 'NB', 'P': 'N', 'PB': 'Z'},
    'NVB': {'NB': 'NVVB', 'N': 'NVVB', 'ZO': 'NVB', 'P': 'NB', 'PB': 'N'}
}

vectors = {
    'NVVB': -32,
    'NVB': -24,
    'NB': -16,
    'N': -8,
    'Z': 0,
    'P': 8,
    'PB': 16,
    'PVB': 24,
    'PVVB': 32,
}
