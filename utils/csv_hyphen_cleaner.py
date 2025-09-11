#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 17:25:14 2025

@author: user
"""

#!/usr/bin/env python3
import sys
import pandas as pd

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input.csv>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = input_file  # overwrite same file; change if you want a new one

# Read CSV as text (no type inference)
df = pd.read_csv(input_file, dtype=str)

# Replace all "-" with "_"
df["ID"] = df["ID"].apply(lambda x: x.replace("-", "_") if isinstance(x, str) else x)

# Save back to CSV
df.to_csv(output_file, index=False)
print(f"Replaced '-' with '_' in {output_file}")
