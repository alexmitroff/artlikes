# artlikes
Get likes from artstation user profile or search term

## Quick start

**You will need Python >= 3.6**

```bash
git clone https://github.com/alexmitroff/artlikes.git
python3.6 -m venv .artlikes-env
source .artlikes/bin/activate
pip install -r requirements.txt

cd artlikes
# Usage
python likes2csv.py -u aka_alarm #by user
python likes2csv.py -s snake #by search term
# Returns file YYYYMMDDHHMM_artstation_<user or term>.csv

python csv2plot.py path/to/file.csv path/to/file2.csv
# Returns file YYYYMMDDHHMM_artstation_<user or term>.svg
```