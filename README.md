# GeoJSON io

## Install

Clone this repo and go the folder.

Install the requirements: 

```
   pip install -r requirements.txt 
   ```
## Config

#### Create your access token:

* Go to https://github.com/settings/tokens
* Click the button 'Generate new token'
* Choose a name in the 'Note' input
* Mark JUST the checkbox gist - Create gists
* In the end of the page click Generate token
* Copy your token!

* Edit the gitauth.txt file and put your token on the first line


## Run

You are good to go. Now, run: 
   ```
   python geojsonio.py yourdataset.geojson
   ```

If the dataset is too large it will create a gist, otherwise it will just open the browser and render the map.
