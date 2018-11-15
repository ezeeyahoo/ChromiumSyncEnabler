# ChromiumSyncEnabler
Secured way to enable sync for official/non-official(local build) and stable/non-stable version of Chromium on Mac while keeping APIs safe, without globally exposing keys.

# How to run

Before running, you must have Google API keys [(steps 6 to 10)](https://gist.github.com/ezeeyahoo/dc4bdd250c6c6468959e107ddaef53f4)

You can also use keys used in chromium for linux platform:-
```bash
export GOOGLE_API_KEY="AIzaSyCkfPOPZXDKNn8hhgu3JrA62wIgC93d44k"
export GOOGLE_DEFAULT_CLIENT_ID="811574891467.apps.googleusercontent.com"
export GOOGLE_DEFAULT_CLIENT_SECRET="kdloedMFGdGla2P1zacGjAQh"
```

Install Chromium. 
You can get it using brew (recommended no doubt)
Stable release:-
```
brew cask install freesmug-chromium
```
Unstable release:-
```
brew cask install chromium
```

OR

from [macchrome](https://github.com/macchrome/) repo. Any version will do, should not be NOSYNC(check sync/nosync in the names)

```bash
git clone https://github.com/ezeeyahoo/ChromiumSyncEnabler.git
cd ChromiumSyncEnabler
```

Run using any python on Mac, e.g.:-
```bash
python ./ChromiumSyncEnabler.py
```
OR
```bash
python3 ./ChromiumSyncEnabler.py
```

NOTE: If you relocate app to $HOME/Applications or /Applications then re-run to reactivate.

Follow on-screen instructions

# Report Issues
Write [here](https://github.com/ezeeyahoo/ChromiumSyncEnabler/issues)

# To Do
Py2App
GUI
