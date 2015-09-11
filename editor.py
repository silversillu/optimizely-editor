import optimizely # for Optimizely API acess
import os # To read and write files
import sys # To read and write files
import os.path, time # For editing files

print 'Please insert your TOKEN. (Could be found on optimizely.com/tokens)'
print 'Saved tokens:'
print '|for Diamondcandles type DC |'
token = raw_input('- ')
if token.lower() == "dc":
    token = "2da375afde0f348bf1e45fc4c0d97385:911add2d"
client = optimizely.Client(token)

# POSSIBLE ACTIONS:
# Get existing experiment
def getExperiment():
    print "Insert experiment ID: "
    experimentID = int(raw_input('- '))
    experiment = client.Experiments.get(experimentID)
    experimentJS = experiment.__dict__['custom_js']
    experimentCSS = experiment.__dict__['custom_css']
    experimentName = str(experiment.__dict__['description'])
    # if no such folder exists on computer - create it
    if not os.path.exists(experimentName):
        os.makedirs(experimentName)
    # If file doesn't exist, create it and if exists update its content.
    files = [] # array for files that could be edited
    experimentJSfile = open(experimentName + '/experiment.js', 'w')
    experimentJSfile.write(experimentJS)
    experimentJSfile.close()
    files.append(experimentName + '/experiment.js')
    experimentCSSfile = open(experimentName + '/experiment.css', 'w')
    experimentCSSfile.write(experimentCSS)
    experimentCSSfile.close()
    files.append(experimentName + '/experiment.css')
    # Create backup files which wont be upladed to Optimizely
    experimentJSfile = open(experimentName + '/experiment(backup).js', 'w')
    experimentJSfile.write(experimentJS)
    experimentJSfile.close()
    experimentCSSfile = open(experimentName + '/experiment(backup).css', 'w')
    experimentCSSfile.write(experimentCSS)
    experimentCSSfile.close()
    # Get the variations
    num_variations = len(experiment.__dict__['variation_ids'])
    print "There are ", num_variations , "variations in this experiment." 
    for i in range(num_variations):
        variationID = experiment.__dict__['variation_ids'][i]
        # print "Collecting information for variation:", variationID
        # Create folder with variation.js for every variation
        variation = client.Variations.get(variationID)
        variationName = str(variation.__dict__['description'])
        path = experimentName + "/"
        if not os.path.exists(experimentName + "/" + variationName):
            os.makedirs(experimentName + "/" + variationName)
        variationJS = variation.__dict__['js_component']
        variationJSfile = open(experimentName + '/' + variationName + '/variation.js', 'w')
        variationJSfile.write(variationJS)
        variationJSfile.close()
        files.append(experimentName + '/' + variationName + '/variation.js') # For editing files
        # Create backup files which wont be upladed to Optimizely
        variationJSfile = open(experimentName + '/' + variationName + '/variation(backup).js', 'w')
        variationJSfile.write(variationJS)
        variationJSfile.close()
        print "Indexed variation : ", variationName
    #print "Collected files are : ", files
    print "___Your files are ready to edit \nClose the Terminal when done editing___"
    changes = {} # Dictionary for filepaths that must be checked for changes
    for i in range(len(files)):
        changes[files[i]]=os.path.getmtime(files[i])
    editingExperiment = True

    while editingExperiment == True:
        for f in files:
            if changes.get(f) < os.path.getmtime(f):
                changes[f] = os.path.getmtime(f)
                if "experiment.js" in f:
                    thisFileContent = open(f , 'r')
                    experiment.custom_js = thisFileContent.read()
                    thisFileContent.close()
                    experiment.save()
                    print "File {} has been modified".format(f)
                elif "experiment.js" in f:
                    thisFileContent = open(f , 'r')
                    experiment.custom_css = thisFileContent.read()
                    thisFileContent.close()
                    experiment.save()
                    print "File {} has been modified".format(f)
                elif "variation.js" in f:
                    thisFileContent = open(f , 'r')
                    variation.js_component = thisFileContent.read()
                    thisFileContent.close()
                    variation.save()
                    print "File {} has been modified".format(f)
            # else:
                # print "No changes found, checking again." # For debugging
        time.sleep(10) # How often to check for modifications

getExperiment()

# __________________ END "GET EXPERIMENT FUNCTION" ____________________

# New experiment
# New variation

# Choose next action function
"""
def nextAction():
    print "CHOOSE YOUR ACTION - type letter and press enter to choose \n - E - index and edit experiment"
    nextActionName = raw_input('- ')
    if nextActionName == "E" or nextActionName == "e":
        getExperiment()
    nextAction()

nextAction()
"""