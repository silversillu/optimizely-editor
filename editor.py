import optimizely # for Optimizely API acess
import os # To read and write files
import sys # To read and write files
import os.path, time # For editing files
from time import gmtime, strftime # for backup file names

print 'Please insert your TOKEN. (Could be found on optimizely.com/tokens)'
# Saved tokens - feel free to add more

savedTokens = open('saved tokens.txt', 'r')
savedTokensContent = savedTokens.readlines()
savedTokens.close()
print "SAVED TOKENS:"
print 'NAME and  KEY --> to choose, type "KEY" and press enter'
print "________________________________________________________"
for line in savedTokensContent:
    lineContent = line.split('-')
    print "Name: " + lineContent[0] + ' Key: ' + lineContent[1]
print "Insert Token or Key"
token = raw_input('- ')
for line in savedTokensContent:
    if token.lower() in lineContent[1]:
        token = lineContent[2].replace('\n', '')
        
if token.lower() == "":
    token = ""
client = optimizely.Client(token)

# POSSIBLE ACTIONS:
# Get existing experiment
def getExperiment():
    print "______________________"
    print "Insert experiment ID: "
    experimentID = int(raw_input('- '))
    experiment = client.Experiments.get(experimentID)
    experimentJS = experiment.__dict__['custom_js']
    experimentCSS = experiment.__dict__['custom_css']
    experimentName = str(experiment.__dict__['description'])
    experimentName = experimentName.replace('/', '-') # To not mess up the path
    # if no such folder exists on computer - create it
    if not os.path.exists(experimentName):
        os.makedirs(experimentName)
    # Folder for backups
    if not os.path.exists(experimentName + "/backups"):
        os.makedirs(experimentName + "/backups")
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
    experimentJSfile = open(experimentName + '/backups/experiment-' + strftime('%Y-%m-%d_%H-%M-%S', gmtime()) + '.js', 'w')
    experimentJSfile.write(experimentJS)
    experimentJSfile.close()
    experimentCSSfile = open(experimentName + '/backups/experiment-' + strftime('%Y-%m-%d_%H-%M-%S', gmtime()) + '.css', 'w')
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
        variationName = variationName.replace('/', '-') # To not mess up the path
        path = experimentName + "/"
        if not os.path.exists(experimentName + "/" + variationName):
            os.makedirs(experimentName + "/" + variationName)
        variationJS = variation.__dict__['js_component']
        variationJSfile = open(experimentName + '/' + variationName + '/variation.js', 'w')
        variationJSfile.write(variationJS)
        variationJSfile.close()
        files.append(experimentName + '/' + variationName + '/variation.js') # For editing files
        # Create backup files which wont be upladed to Optimizely
        variationJSfile = open(experimentName + '/backups/variation-' + strftime('%Y-%m-%d_%H-%M-%S', gmtime()) + '.js', 'w')
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
