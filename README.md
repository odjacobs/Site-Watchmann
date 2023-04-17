# Site-Watchmann  
Monitors webpages for changes in links and posts updates to Discord through a webhook  
# Configuration  
Configuration is done insode of config.json. Just follow [config-example.json](config-example.json)  
# Running  
This script can be ran in two ways.  
## Docker
```
docker build -t watchmann:latest .
docker run -d -v /path/to/links.sqlite3:/opt/Watchmann/links.sqlite3 -v /path/to/config.json:/opt/Watchmann/config.json --name watchmann watchmann:latest
```
## Not Docker
Linux  
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python watchmann.py
```
Windows  
```
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python watchmann.py
```
# License
This project is licensed under the GNU General Public License version 3.0. See [LICENSE](LICENSE) for details.