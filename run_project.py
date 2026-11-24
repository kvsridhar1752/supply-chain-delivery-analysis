from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
generator = root / 'data' / 'generate_data.py'
source = generator.read_text(encoding='utf-8')
source = source.replace('order_dates.dt.month', 'order_dates.month')
generator.write_text(source, encoding='utf-8')
for script in ['data/generate_data.py', 'analysis/delivery_analysis.py']:
    subprocess.run([sys.executable, script], cwd=root, check=True)
print('Generated dashboard and KPI CSVs in output/. Use these results, not unverified README figures.')
