============
geojsonio.py
============

1. Clone this repo and go the folder.

2. Install the requirements: 
   ```
   pip install -r requirements.txt 
   ```
   
3. Create your access token:
3.1 Go to https://github.com/settings/tokens
3.2 Click the button 'Generate new token'
3.3 Choose a name in the 'Note' input
3.4 Mark JUST the checkbox gist - Create gists
3.5 In the end of the page click Generate token
3.6 Copy your token!

4. Edit the gitauth.txt file and put your token on the first line

5.You are good to go. Now, run: 
   ```
   python geojsonio.py yourdataset.geojson
   ```

If the dataset is too large it will create a gist, otherwise it will just open the browser and render the map.
