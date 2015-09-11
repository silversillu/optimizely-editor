# optimizely-editor
Optimizely Editor - Python

Documentation
-------------

Optimizely Editor for local editing.

To run the program you need to:

1. Have Python on your device http://www.python.org/download/
  - When installing make sure to check "Add Python to your path"
2. Install PIP
  - How to do it on Windows: http://arunrocks.com/guide-to-install-python-or-pip-on-windows/
3. Install Optimizely using PIP
  - $ pip install https://github.com/optimizely/optimizely-client-python/archive/master.zip

-------------------------------
How to use the Python Optimizely editor for local editing using your favorite tools

1. You need to know the API Token for the project you want to edit - http://optimizely.com/tokens
  - You can save them, so that you don't have to insert them every time
2. You need to know the ID of the experiment you are going to edit
3. After inserting API Token and experiment ID the program indexes and creates the files and folders needed:
  - Experiment folder
      - Experiment.css
      - Experiment.js
      - Variation folders
          - Variation.js
  - (also a backup file for each file)
4. After the program said "Your files are ready to edit" you can open and edit the file, after you save the file it's going to be uploaded to Optimizely automatically
5. When done with the editing: close the program.

How to add new saved token
----------
1. Open "saved tokens.txt"
2. Add new line following the example given
  - tokenAccountName-tokenKey-token

