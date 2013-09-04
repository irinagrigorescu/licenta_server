__author__ = 'Irina'

# IMPORTS
import ESAsimilarity
from django.views.generic import list
from nltk.stem import porter
import re
from string import *
from pprint import pprint
from collections import defaultdict
import math
import MySQLdb
import operator
from Enviro.models import User

# CONSTANTS
ENGLISH_STOP_WORDS = ["specify", "between", "whence", "i've", "hopefully", "followed", "gotten", "thus", "does", "sure", "saying", "beside", "course", "necessary", "you", "having", "viz", "near", "appropriate", "am", "an", "while", "down", "below", "as", "at", "sensible", "different", "whereunto", "placed", "y", "be", "hereby", "out", "wherein", "overall", "how", "see", "by", "already", "seven", "whose", "a", "b", "c", "d", "e", "f", "g", "c'mon", "cause", "j", "k", "co", "himself", "beforehand", "o", "p", "former", "r", "s", "second", "u", "v", "w", "x", "whichever", "brief", "we'd", "across", "whereafter", "using", "did", "let's", "whom", "do", "got", "eight", "name", "likely", "need", "might", "merely", "seemed", "clearly", "gone", "t's", "certain", "inasmuch", "wish", "its", "him", "who's", "et", "she", "isn't", "nine", "ex", "normally", "try", "take", "own", "being", "could", "becoming", "either", "currently", "taken", "without", "for", "indicated", "exactly", "contain", "well", "c's", "rather", "h", "hello", "the", "believe", "appreciate", "l", "indicates", "n", "entirely", "whereat", "q", "looking", "where", "go", "t", "were", "just", "someone", "ain't", "some", "z", "weren't", "th", "ourselves", "anyone", "can't", "howbeit", "sent", "hi", "doesn't", "cannot", "to", "noone", "associated", "selves", "though", "sometime", "usually", "wherefrom", "that's", "went", "herein", "your", "except", "even", "afterwards", "here's", "if", "ever", "once", "inward", "according", "in", "four", "whereby", "twice", "causes", "it", "corresponding", "whensoever", "insofar", "aside", "became", "behind", "i", "despite", "with", "whatsoever", "especially", "concerning", "nobody", "they'd", "m", "us", "a's", "perhaps", "whole", "eg", "awfully", "onto", "namely", "relatively", "able", "wherever", "ignored", "thorough", "may", "third", "have", "think", "example", "everyone", "tends", "however", "off", "enough", "possible", "they're", "somewhat", "sorry", "you'd", "something", "nevertheless", "than", "com", "self", "anyway", "truly", "we've", "use", "vs", "won't", "anybody", "tell", "happens", "said", "via", "etc", "appear", "took", "me", "less", "lest", "specified", "three", "new", "all", "whereto", "outside", "although", "that", "still", "moreover", "hereupon", "we", "my", "ok", "certainly", "don't", "reasonably", "should", "looks", "nd", "fifth", "ones", "consider", "couldn't", "thereby", "obviously", "formerly", "against", "thence", "become", "whilst", "around", "useful", "didn't", "within", "throughout", "and", "oh", "mostly", "after", "like", "on", "respectively", "whatever", "or", "best", "over", "says", "unfortunately", "various", "any", "they've", "comes", "better", "provides", "lately", "we'll", "thereafter", "going", "very", "definitely", "yourself", "else", "each", "which", "because", "secondly", "must", "whomever", "thanx", "always", "want", "downwards", "you're", "regarding", "let", "right", "amongst", "thereupon", "contains", "six", "latter", "further", "qv", "themselves", "old", "they", "their", "wherewith", "almost", "accordingly", "rd", "re", "presumably", "together", "novel", "toward", "sub", "consequently", "during", "probably", "neither", "ie", "such", "whoever", "allows", "two", "sup", "are", "upon", "inner", "theirs", "alone", "so", "along", "many", "into", "is", "when", "meanwhile", "there", "you've", "one", "least", "been", "seems", "came", "ask", "seem", "anywhere", "saw", "whereof", "but", "anything", "these", "them", "then", "therein", "had", "later", "same", "containing", "theres", "there's", "following", "wasn't", "mainly", "last", "un", "has", "up", "needs", "this", "look", "yours", "hither", "cant", "unlikely", "ours", "zero", "whomsoever", "everywhere", "seeing", "first", "five", "everything", "whosoever", "indicate", "per", "among", "maybe", "thats", "que", "changes", "seen", "through", "asking", "where's", "would", "non", "soon", "willing", "nor", "sometimes", "not", "unto", "particular", "now", "under", "shouldn't", "it'll", "i'll", "specifying", "follows", "never", "anyhow", "often", "keep", "yet", "he's", "thank", "tries", "somebody", "whenever", "away", "way", "what's", "next", "little", "itself", "myself", "described", "yourselves", "beyond", "another", "come", "thanks", "ought", "we're", "uucp", "he", "other", "okay", "her", "far", "every", "available", "whereupon", "particularly", "wouldn't", "seeming", "thoroughly", "shall", "latterly", "whither", "seriously", "hence", "keeps", "none", "since", "towards", "everybody", "they'll", "serious", "help", "instead", "known", "getting", "trying", "i'd", "aren't", "knows", "allow", "our", "elsewhere", "i'm", "anyways", "hasn't", "more", "get", "regardless", "albeit", "greetings", "until", "those", "again", "welcome", "others", "know", "you'll", "much", "whereon", "value", "wants", "doing", "furthermore", "regards", "given", "too", "before", "both", "done", "most", "indeed", "forth", "it'd", "considering", "tried", "becomes", "about", "no", "his", "goes", "it's", "few", "besides", "actually", "was", "above", "yes", "what", "somewhere", "from", "really", "only", "liked", "hadn't", "immediate", "unless", "haven't", "otherwise", "nearly", "edu", "thru", "hardly", "wonder", "of", "used", "who", "plus", "somehow", "mean", "nowhere", "also", "why", "uses", "nothing", "can", "will", "apart", "whether", "ltd", "gets", "inc", "whichsoever", "herself", "whereinto", "whereas", "kept", "please", "say", "hereafter", "here", "therefore", "quite", "gives", "several", "hers"]
STEMMER = porter.PorterStemmer()
cat = "category"
catLink = "categorylinks"
wiki_cat = "wiki_cat"
wiki_taxonomy = "wiki_taxonomy"
articledb = "articles"
parentIDCat = 473635
childIDCat = 473639


# Prepare SQL query
# 0. Retrieve article names from articles
getArticleName = "select title from " + articledb + " where id in ("
# 1. Retrieve category names from category sql file (cat_id, cat_title)
getCatName = "select cat_title from " + cat + " where cat_id = 1"
# 2. Retrieve category names from wiki_cat sql file (id, name)
getWikiCatName = "select name from " + wiki_cat + " where id = 1"
# 3. Retrieve category names included in a certain page from categorylinks sql file (cl_from, cl_to)
getCatFromPagesNames = "select cl_to from " + catLink + " where cl_from = 12"
# 4. Retrieve parent categories of a certain category (parent, child)
getParentCat = "select parent from " + wiki_taxonomy + " where child = 2"

def stepFunction(number):
	if number > 0:
		return 1
	else:
		return -1

def sigmoidFunction(number):
	return 1 / (1 + math.exp(-number))

#termlist = ['computers', 'algorithms', 'networking', 'embedded']
## GETTING TOP N IDS NEEDED
def getArticleIDS(listOfTerms, n):
    # Applying FILTERS
    ## LowerCase Filter: Set all letters in the string to lower case
    listOfTerms = listOfTerms.lower()
    listOfTerms.replace("-"," ")
    listOfTerms.replace("(","")
    listOfTerms.replace(")","")
    listOfTerms.replace("/","")

    ## Tokenizer filter
    tokenizer = re.compile("[' ,]")
    listOfTerms = tokenizer.split(listOfTerms)

    # Length filter, StopWord filter, 3 x PorterStemmer
    # Query 1
    i = 0
    while i < len(listOfTerms) :
        if listOfTerms[i] in ENGLISH_STOP_WORDS or len(listOfTerms[i]) < 3 or len(listOfTerms[i]) > 100:
            del listOfTerms[i]
        else:
            listOfTerms[i] = STEMMER.stem_word(STEMMER.stem_word(STEMMER.stem_word(listOfTerms[i])))
            i += 1

    # COMPUTE CONCEPT VECTORS
    conceptVector = ESAsimilarity.getConceptVector(listOfTerms)
    conceptVectorAux = sorted(conceptVector.iteritems(), key=operator.itemgetter(1))
    conceptVectorAux.reverse()
    print conceptVectorAux

    # GET TOP N CONCEPTS
    articles = []
    if len(conceptVectorAux) < n:
        for i in range(0, len(conceptVectorAux)):
            articles.append(conceptVectorAux[i])
    else:
        for i in range(0, n):
            articles.append(conceptVectorAux[i])
    print articles
    return articles

def prepareSQLqueryArticleNames(articles):
    # Prepare sql query for getting article names
    getArticleName = "select * from " + articledb + " where id in ("
    for i in range(len(articles)):
        if i == len(articles) - 1:
            getArticleName += str(articles[i][0]) + ")"
        else:
            getArticleName += str(articles[i][0]) + ", "
    print "\n\n---->Select statement for getting article names that reside within the articles ids provided"
    print getArticleName
    return getArticleName

def prepareSQLqueryCatFromPagesNames(articleID):
    getCatFromPagesNames = "select cl_from, cl_to from " + catLink + " where cl_from in ("
    for i in range(len(articleID)):
        if i == len(articleID) - 1:
            getCatFromPagesNames += str(articleID[i]) + ")"
        else:
            getCatFromPagesNames += str(articleID[i]) + ", "
    print "\n\n---->Select statement for getting categories that reside within the article ids provided"
    print getCatFromPagesNames
    return getCatFromPagesNames

def prepareSQLqueryCatIds(articleCategoryMap):
    getCategoryIds = "select cat_id, cat_title from " + cat + " where cat_title in ('"
    for key, value in articleCategoryMap.iteritems():
        for i in value:
            getCategoryIds += i + "', '"
    getCategoryIds = getCategoryIds[:-3]
    getCategoryIds += ")"
    print "\n\n---->Select statement for getting a map between cat_id and cat_title"
    print getCategoryIds
    return getCategoryIds



def sqlConnection(query, cursorType, message, typeOfSql):
    aux = dict()

    if typeOfSql == 1:
        try:
            cursorType.execute(query)
            results = cursorType.fetchall()
            for row in results:
                aux[int(row[0])] = row[1]
        except:
            print "Error in fetching results"
        print message
        pprint(aux)

    if typeOfSql == 2:
        try:
            cursorType.execute(query)
            results = cursorType.fetchall()
            for row in results:
                if row[0] not in aux.keys():
                    a = []
                    a.append(row[1])
                    aux[int(row[0])] = (a)
                else:
                    aux[int(row[0])].append(row[1])
                #print '%i - %s' % (row[0], row[1])
        except:
            print "Error in fetching results"
        print message
        pprint(aux)

    return aux

def deleteUnimportantValues(catIdTitleMap):
    deletedValues = []
    for key, value in catIdTitleMap.iteritems():
        if key > childIDCat:
            deletedValues.append(value)
    return deletedValues

def deleteUnimportantKeys(catIdTitleMap):
    deletedKeys = []
    for key, value in catIdTitleMap.iteritems():
        if key > childIDCat:
            deletedKeys.append(key)
    return deletedKeys

## Look through catIdTitleMap.values() and discard those > child_limit
def restrainCategories(deletedKeys, catIdTitleMap):
    for key in deletedKeys:
        del catIdTitleMap[key]

    print "\n\n\n\nModified category ids:"
    pprint(catIdTitleMap)
    return catIdTitleMap

## Look through articleCategoryMap.values() and discard those > child_limit
def restrainCategoryArticles(deletedValues, articleCategoryMap):
    for key, value in articleCategoryMap.iteritems():
        for word in deletedValues:
            articleCategoryMap[key] = filter(lambda a: a != word, articleCategoryMap[key])

    print "\n\nModified page_ids with categories:"
    pprint(articleCategoryMap)
    return articleCategoryMap

def countNumberOfTimesEachCatAssocArticle(articleCategoryMap):
    noPagesPerCateg = dict()
    for key, values in articleCategoryMap.iteritems():
        for v in values:
            if v not in noPagesPerCateg.keys():
                noPagesPerCateg[v] = 0
            else:
                noPagesPerCateg[v] = noPagesPerCateg[v] + 1
    print "\n\n---->For each category i have the number of times it appears in the articles"
    noPagesPerCateg = sorted(noPagesPerCateg.iteritems(), key=operator.itemgetter(1))
    noPagesPerCateg.reverse()
    #noPagesPerCateg = dict(noPagesPerCateg)
    pprint(noPagesPerCateg)
    return noPagesPerCateg

def prepareSQLqueryWikiCatIds(noPagesPerCateg, n):
    wikicategorynames = []
    i = 0
    for wiki in noPagesPerCateg:
        i += 1
        if wiki[1] > 0 or i <= n:
            wikicategorynames.append(wiki[0])
    print wikicategorynames
    sqlForIds = "select * from " + wiki_cat + " where name in ('"
    for w in wikicategorynames:
        sqlForIds += w.replace('_', ' ') + "', '"
    sqlForIds = sqlForIds[:-3]
    sqlForIds += ")"
    print sqlForIds
    return sqlForIds

## THE SPREADING ACTIVATION ALGORITHM
def spreadingActivationAlgo(listOfTerms, userId, n, method):
    # DATABASE CONNECTIONS
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "", "wiki")
    db2 = MySQLdb.connect("localhost", "root", "", "wikiprep")
    # Prepare a cursor object
    cursor = db.cursor()
    cursor2 = db2.cursor()
    ################################################
    # 1. Get top N Article IDS for the list of terms
    articles = []
    articles = getArticleIDS(listOfTerms, n)

    if (articles is None):
        current_user = User.objects.get(id=userId)
        current_user.tag_set_improved = ""
        current_user.save()
        return "Nothing Found"

    ###########################################
    # 2. Fetching needed data from the database
    ## 2.1 Article Names
    articleIdMap = dict()
    getArticleName = prepareSQLqueryArticleNames(articles)
    articleIdMap = sqlConnection(getArticleName, cursor2, "\n\n---->A dictionary with keys as article ids and values as article names", 1)
    ### 2.1.1 Article ID
    articleID = []
    for key in articleIdMap.keys():
        articleID.append(key)
    pprint(articleID)

    ## 2.2 Get Categories that reside within the article ids
    articleCategoryMap = dict()
    getCatFromPagesNames = prepareSQLqueryCatFromPagesNames(articleID)
    articleCategoryMap = sqlConnection(getCatFromPagesNames, cursor, "\n\n---->A dictionary with keys as article ids and values as a list of categories", 2)

    ## 2.3 Get map between category id and category title (cat_id, cat_title)
    catIdTitleMap = dict()
    getCategoryIds = prepareSQLqueryCatIds(articleCategoryMap)
    catIdTitleMap = sqlConnection(getCategoryIds, cursor, "\n\n---->A dictionary with keys as category ids and values as category titles", 1)
    #####
    ## 2.3.1 Look through catIdTitleMap.values() and discard those > child_limit
    ## and save deleted values
    deletedValues = deleteUnimportantValues(catIdTitleMap)
    deletedKeys = deleteUnimportantKeys(catIdTitleMap)
    catIdTitleMap = restrainCategories(deletedKeys, catIdTitleMap)
    articleCategoryMap = restrainCategoryArticles(deletedValues, articleCategoryMap)
    #####
    ## 2.3.2 Count the number of times each Wikipedia category was associated with one of the N pages
    noPagesPerCateg = countNumberOfTimesEachCatAssocArticle(articleCategoryMap)

    ## 2.4 Find their ids within the wiki_cat db
    initialCatIdNodes = dict()
    sqlForIds = prepareSQLqueryWikiCatIds(noPagesPerCateg, n)
    initialCatIdNodes = sqlConnection(sqlForIds, cursor, "\n\n---->Ids for wiki categories", 1)

    ######################################
    ####### SPREADING ACTIVATION #########
    ######################################

    ############################# GETTING ALL THE INFORMATION NEEDED
    ## 1. INITIAL NODES
    print "\n\n\n\nINITIAL NODES ARE:"
    pprint(initialCatIdNodes)

    ## 2. GETTING THE INITIAL LINKS
    sqlFor1Links = "select parent, child from " + wiki_taxonomy + " where child in ("
    for key in initialCatIdNodes.keys():
        sqlFor1Links += str(key) + ", "
    sqlFor1Links = sqlFor1Links[:-2]
    sqlFor1Links += ")"
    #print sqlFor1Links
    firstLinks = dict()
    try:
        cursor.execute(sqlFor1Links)
        results = cursor.fetchall()
        for row in results:
            if int(row[0]) not in firstLinks.keys():
                firstLinks[int(row[0])] = []
                firstLinks[int(row[0])].append(int(row[1]))
            else:
                firstLinks[int(row[0])].append(int(row[1]))
    except:
        print "Error in fetching results"
    print "\n\nLinks between initial nodes and first degree neighbours"
    pprint(firstLinks)

    ## 3. SECOND-DEGREE NEIGHBOURS -- LOOKING FOR THEIR NAMES IN THE WIKI_CAT DATABASE
    sqlFor1Parents = "select * from " + wiki_cat + " where id in ("
    for key in firstLinks.keys():
        sqlFor1Parents += str(key) + ", "
    sqlFor1Parents = sqlFor1Parents[:-2]
    sqlFor1Parents += ")"
    #print sqlFor1Parents
    secondCatIdNodes = dict()
    try:
        cursor.execute(sqlFor1Parents)
        results = cursor.fetchall()
        for row in results:
            secondCatIdNodes[int(row[0])] = row[1]
    except:
        print "Error in fetching results"
    print "\n\nSECOND-DEGREE NEIGHBOURS ARE:"
    pprint(secondCatIdNodes)


    ## 4. GETTING THE SECOND DEGREE LINKS
    sqlFor2Links = "select * from " + wiki_taxonomy + " where child in ("
    for key in secondCatIdNodes.keys():
        sqlFor2Links += str(key) + ", "
    sqlFor2Links = sqlFor2Links[:-2]
    sqlFor2Links += ")"
    #print sqlFor2Links
    secondLinks = dict()
    try:
        cursor.execute(sqlFor2Links)
        results = cursor.fetchall()
        for row in results:
            if int(row[0]) not in secondLinks.keys():
                secondLinks[int(row[0])] = []
                secondLinks[int(row[0])].append(int(row[1]))
            else:
                secondLinks[int(row[0])].append(int(row[1]))
    except:
        print "Error in fetching results"
    print "\n\nLinks between second nodes and third degree neighbours"
    pprint(secondLinks)


    ## 5. THIRD-DEGREE NEIGHBOURS -- LOOKING FOR THEIR NAMES IN THE WIKI_CAT DATABASE
    sqlFor2Parents = "select * from " + wiki_cat + " where id in ("
    for key in secondLinks.keys():
        sqlFor2Parents += str(key) + ", "
    sqlFor2Parents = sqlFor2Parents[:-2]
    sqlFor2Parents += ")"
    #print sqlFor2Parents
    thirdCatIdNodes = dict()
    try:
        cursor.execute(sqlFor2Parents)
        results = cursor.fetchall()
        for row in results:
            thirdCatIdNodes[int(row[0])] = row[1]
    except:
        print "Error in fetching results"
    print "\n\nTHIRD-DEGREE NEIGHBOURS ARE:"
    pprint(thirdCatIdNodes)

    ## 6. GETTING THE THIRD DEGREE LINKS
    sqlFor3Links = "select * from " + wiki_taxonomy + " where child in ("
    for key in thirdCatIdNodes.keys():
        sqlFor3Links += str(key) + ", "
    sqlFor3Links = sqlFor3Links[:-2]
    sqlFor3Links += ")"
    print sqlFor3Links
    thirdLinks = dict()
    try:
        cursor.execute(sqlFor3Links)
        results = cursor.fetchall()
        for row in results:
            if int(row[0]) not in thirdLinks.keys():
                thirdLinks[int(row[0])] = []
                thirdLinks[int(row[0])].append(int(row[1]))
            else:
                thirdLinks[int(row[0])].append(int(row[1]))
    except:
        print "Error in fetching results"
    print "\n\nLinks between third nodes and fourth degree neighbours"
    pprint(thirdLinks)

    ## 7. FOURTH-DEGREE NEIGHBOURS -- LOOKING FOR THEIR NAMES IN THE WIKI_CAT DATABASE
    sqlFor3Parents = "select * from " + wiki_cat + " where id in ("
    for key in thirdLinks.keys():
        sqlFor3Parents += str(key) + ", "
    sqlFor3Parents = sqlFor3Parents[:-2]
    sqlFor3Parents += ")"
    #print sqlFor3Parents
    fourthCatIdNodes = dict()
    try:
        cursor.execute(sqlFor3Parents)
        results = cursor.fetchall()
        for row in results:
            fourthCatIdNodes[int(row[0])] = row[1]
    except:
        print "Error in fetching results"
    print "\n\nFOURTH-DEGREE NEIGHBOURS ARE:"
    pprint(fourthCatIdNodes)


    db.close()
    db2.close()
    ############################# DONE WITH GETTING ALL THE INFORMATION NEEDED

    #######################################
    ############################# ALGORITHM

    ## METHOD 1
    '''
    Simply count the number of times each Wikipedia category was associated
    with one of the N results
    '''
    if method == "1":
        print "\n\n\n\nMETHOD 1"
        pprint(initialCatIdNodes.values())
        print "\n"
        ##### Write to tag_set_improved in user table at id = userId

        method1 = []
        for key, value in initialCatIdNodes.iteritems():
                method1.append(value)

        current_user = User.objects.get(id=userId)
        current_user.tag_set_improved = method1
        current_user.save()
        return method1

    ## METHOD 2
    '''
    The former Wikipedia categories will be used as initial nodes in the
    Wikipedia Category Graph.
    '''

    ## METHOD 2 - 2 pulses
    '''
    We calculate the input and output functions for the second-degree neighbours
    '''
    if method == "2.1" or method == "2.2":
        print "\n\n\n\nMETHOD 2 - 1 pulse"
        kPulses = 2
        # sum of outputs that come from the initial nodes and link with the ones from the second degree nodes
        inputVector = dict()
        # use an activation function on the input and divide by number of pulses times out degree of node
        outputVector = dict()
        # initialize dictionaries with keys from secondCatIdNodes
        for k in secondCatIdNodes.keys():
            inputVector[k] = 0
            outputVector[k] = 0
        #pprint(inputVector)
        #pprint(outputVector)
        # The initial nodes are assigned with integer number 1 as output links
        for key in firstLinks.keys():
            inputVector[key] = len(firstLinks[key])
        #print "Input vectors"
        #pprint(inputVector)
        # The output nodes.
        # First, assign out degree for each node
        for val in secondLinks.values():
            for key in outputVector.keys():
                if key in val:
                    outputVector[key] += 1
        # Second, multiply by the pulse number
        for key in outputVector.keys():
            outputVector[key] = outputVector[key] * kPulses
        # Third, compute activation function on input nodes and divide by output nodes
        for key in inputVector.keys():
            if outputVector[key] != 0:
                outputVector[key] = float(stepFunction(inputVector[key])) / outputVector[key]
        #print "Output vectors"
        #pprint(outputVector)
        # Compute Activation SCORES for each output
        for key in outputVector.keys():
            outputVector[key] = float(stepFunction(outputVector[key]))
        #print "Activated outputs"
        #pprint(outputVector)
        aux_method2sort = sorted(outputVector.iteritems(), key=operator.itemgetter(1))
        aux_method2sort.reverse()
        #pprint(aux_method2sort)
        method2_2pulses = []

        for l in aux_method2sort:
            for key, value in secondCatIdNodes.iteritems():
                if key == l[0]:
                    method2_2pulses.append(value)
        pprint(method2_2pulses)
        pprint(aux_method2sort)
        print "\n"

        ##### Write to tag_set_improved in user table at id = userId
        current_user = User.objects.get(id=userId)
        if method != "2.2":
            if len(method2_2pulses) >= n:
                current_user.tag_set_improved = method2_2pulses[0:n]
                current_user.save()
                return method2_2pulses[0:n]
            else:
                current_user.tag_set_improved = method2_2pulses
                current_user.save()
                return method2_2pulses


    #################################
    ## METHOD 2 - 3 pulses
    '''
    We calculate the input and output functions for the third-degree neighbours
    '''
    if method == "2.2":
        print "\n\n\n\nMETHOD 2 - 2 pulses"
        kPulses = 3
        # sum of outputs that come from the initial nodes and link with the ones from the second degree nodes
        inputVector2 = dict()
        # use an activation function on the input and divide by number of pulses times out degree of node
        outputVector2 = dict()
        # initialize dictionaries with keys from secondCatIdNodes
        for k in thirdCatIdNodes.keys():
            inputVector2[k] = 0
            outputVector2[k] = 0
        #pprint(inputVector2)
        #pprint(outputVector2)
        ## The input vectors are sums of the output vectors
        for key, val in secondLinks.iteritems():
            for v in val:
                inputVector2[key] = inputVector2[key] + outputVector[v]
        #print "Input vectors"
        #pprint(inputVector2)

        # The output nodes.
        # First, assign out degree for each node
        for val in thirdLinks.values():
            for key in outputVector2.keys():
                if key in val:
                    outputVector2[key] += 1
        #pprint(outputVector2)
        # Second, multiply by the pulse number
        for key in outputVector2.keys():
            outputVector2[key] = outputVector2[key] * kPulses
        # Third, compute activation function on input nodes and divide by output nodes
        for key in inputVector2.keys():
            if outputVector2[key] != 0:
                outputVector2[key] = float(stepFunction(inputVector2[key])) / outputVector2[key]
        #print "Output vectors"
        #pprint(outputVector2)
        # Compute Activation SCORES for each output
        for key in outputVector2.keys():
            outputVector2[key] = float(stepFunction(outputVector2[key]))
        #print "Activated outputs"
        #pprint(outputVector2)
        aux_method23sort = sorted(outputVector2.iteritems(), key=operator.itemgetter(1))
        aux_method23sort.reverse()
        #pprint(aux_method23sort)
        method2_3pulses = []

        for l in aux_method23sort:
            for key, value in thirdCatIdNodes.iteritems():
                if key == l[0]:
                    method2_3pulses.append(value)
        pprint(method2_3pulses)
        print "\n"

        ##### Write to tag_set_improved in user table at id = userId
        if method == "2.2":
            current_user = User.objects.get(id=userId)
            if len(method2_3pulses) >= n:
                current_user.tag_set_improved = method2_3pulses[0:n]
                current_user.save()
                return method2_3pulses[0:n]
            else:
                current_user.tag_set_improved = method2_3pulses
                current_user.save()
                return method2_3pulses

    ############################# DONE WITH THE ALGORITHM

#termlist = "Oxycodone / paracetamol, Erythromycin, Streptomycin"
#ana = spreadingActivationAlgo(termlist, 2, 5, "2.2")
#print(ana)

