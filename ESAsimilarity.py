from django.core.management import setup_environ
import settings as config
setup_environ(config)

from django.core.exceptions import ValidationError
import array
import struct
import math
import MySQLdb
#import Stemmer
from nltk.stem import porter
from snowballstemmer import english_stemmer
import re

from Enviro.models import Booth, User, BoothSimilarities, UserSimilarities

ENGLISH_STOP_WORDS = ["specify", "between", "whence", "i've", "hopefully", "followed", "gotten", "thus", "does", "sure", "saying", "beside", "course", "necessary", "you", "having", "viz", "near", "appropriate", "am", "an", "while", "down", "below", "as", "at", "sensible", "different", "whereunto", "placed", "y", "be", "hereby", "out", "wherein", "overall", "how", "see", "by", "already", "seven", "whose", "a", "b", "c", "d", "e", "f", "g", "c'mon", "cause", "j", "k", "co", "himself", "beforehand", "o", "p", "former", "r", "s", "second", "u", "v", "w", "x", "whichever", "brief", "we'd", "across", "whereafter", "using", "did", "let's", "whom", "do", "got", "eight", "name", "likely", "need", "might", "merely", "seemed", "clearly", "gone", "t's", "certain", "inasmuch", "wish", "its", "him", "who's", "et", "she", "isn't", "nine", "ex", "normally", "try", "take", "own", "being", "could", "becoming", "either", "currently", "taken", "without", "for", "indicated", "exactly", "contain", "well", "c's", "rather", "h", "hello", "the", "believe", "appreciate", "l", "indicates", "n", "entirely", "whereat", "q", "looking", "where", "go", "t", "were", "just", "someone", "ain't", "some", "z", "weren't", "th", "ourselves", "anyone", "can't", "howbeit", "sent", "hi", "doesn't", "cannot", "to", "noone", "associated", "selves", "though", "sometime", "usually", "wherefrom", "that's", "went", "herein", "your", "except", "even", "afterwards", "here's", "if", "ever", "once", "inward", "according", "in", "four", "whereby", "twice", "causes", "it", "corresponding", "whensoever", "insofar", "aside", "became", "behind", "i", "despite", "with", "whatsoever", "especially", "concerning", "nobody", "they'd", "m", "us", "a's", "perhaps", "whole", "eg", "awfully", "onto", "namely", "relatively", "able", "wherever", "ignored", "thorough", "may", "third", "have", "think", "example", "everyone", "tends", "however", "off", "enough", "possible", "they're", "somewhat", "sorry", "you'd", "something", "nevertheless", "than", "com", "self", "anyway", "truly", "we've", "use", "vs", "won't", "anybody", "tell", "happens", "said", "via", "etc", "appear", "took", "me", "less", "lest", "specified", "three", "new", "all", "whereto", "outside", "although", "that", "still", "moreover", "hereupon", "we", "my", "ok", "certainly", "don't", "reasonably", "should", "looks", "nd", "fifth", "ones", "consider", "couldn't", "thereby", "obviously", "formerly", "against", "thence", "become", "whilst", "around", "useful", "didn't", "within", "throughout", "and", "oh", "mostly", "after", "like", "on", "respectively", "whatever", "or", "best", "over", "says", "unfortunately", "various", "any", "they've", "comes", "better", "provides", "lately", "we'll", "thereafter", "going", "very", "definitely", "yourself", "else", "each", "which", "because", "secondly", "must", "whomever", "thanx", "always", "want", "downwards", "you're", "regarding", "let", "right", "amongst", "thereupon", "contains", "six", "latter", "further", "qv", "themselves", "old", "they", "their", "wherewith", "almost", "accordingly", "rd", "re", "presumably", "together", "novel", "toward", "sub", "consequently", "during", "probably", "neither", "ie", "such", "whoever", "allows", "two", "sup", "are", "upon", "inner", "theirs", "alone", "so", "along", "many", "into", "is", "when", "meanwhile", "there", "you've", "one", "least", "been", "seems", "came", "ask", "seem", "anywhere", "saw", "whereof", "but", "anything", "these", "them", "then", "therein", "had", "later", "same", "containing", "theres", "there's", "following", "wasn't", "mainly", "last", "un", "has", "up", "needs", "this", "look", "yours", "hither", "cant", "unlikely", "ours", "zero", "whomsoever", "everywhere", "seeing", "first", "five", "everything", "whosoever", "indicate", "per", "among", "maybe", "thats", "que", "changes", "seen", "through", "asking", "where's", "would", "non", "soon", "willing", "nor", "sometimes", "not", "unto", "particular", "now", "under", "shouldn't", "it'll", "i'll", "specifying", "follows", "never", "anyhow", "often", "keep", "yet", "he's", "thank", "tries", "somebody", "whenever", "away", "way", "what's", "next", "little", "itself", "myself", "described", "yourselves", "beyond", "another", "come", "thanks", "ought", "we're", "uucp", "he", "other", "okay", "her", "far", "every", "available", "whereupon", "particularly", "wouldn't", "seeming", "thoroughly", "shall", "latterly", "whither", "seriously", "hence", "keeps", "none", "since", "towards", "everybody", "they'll", "serious", "help", "instead", "known", "getting", "trying", "i'd", "aren't", "knows", "allow", "our", "elsewhere", "i'm", "anyways", "hasn't", "more", "get", "regardless", "albeit", "greetings", "until", "those", "again", "welcome", "others", "know", "you'll", "much", "whereon", "value", "wants", "doing", "furthermore", "regards", "given", "too", "before", "both", "done", "most", "indeed", "forth", "it'd", "considering", "tried", "becomes", "about", "no", "his", "goes", "it's", "few", "besides", "actually", "was", "above", "yes", "what", "somewhere", "from", "really", "only", "liked", "hadn't", "immediate", "unless", "haven't", "otherwise", "nearly", "edu", "thru", "hardly", "wonder", "of", "used", "who", "plus", "somehow", "mean", "nowhere", "also", "why", "uses", "nothing", "can", "will", "apart", "whether", "ltd", "gets", "inc", "whichsoever", "herself", "whereinto", "whereas", "kept", "please", "say", "hereafter", "here", "therefore", "quite", "gives", "several", "hers"]
STEMMER_PORTER = porter.PorterStemmer() #english_stemmer.EnglishStemmer # Stemmer.Stemmer('porter')

# Compute user to booth/user similarities
def computeUserSimilarities(action, userId=None, tagSet=None):

    # Get current user information from database
    current_user = User.objects.get(id=userId)
    new_booth_similarities = None
    new_user_similarities = None

    # If an update_profile is required, delete old similarities from databas
    if action == 'update_profile':
        BoothSimilarities.objects.filter(userFrom=current_user).delete()
        UserSimilarities.objects.filter(userFrom=current_user).delete()


    # Get every BOOTH in the system and compute similarity
    print "======COMPUTING BOOTHS SIMILARITY======"
    for booth in Booth.objects.all():
        print "===> BOOTH: " + booth.title
        booth_similarity = getRelatedness(tagSet, booth.tag_set)
        new_booth_similarities = BoothSimilarities(userFrom=current_user, boothTo=booth, similarity=booth_similarity)

        # Perform validation for DB fields
        try:
            new_booth_similarities.full_clean()
        except ValidationError, e:
            return "ComputeSimilarity.Failed"
        # Commit to database
        new_booth_similarities.save()


    # Get every USER in the system and compute similarity
    print "======COMPUTING USERS SIMILARITY======"
    for user in User.objects.all():
        print "===> USER: " + user.name
        user_similarity = getRelatedness(tagSet, user.tag_set)
        new_user_similarities = UserSimilarities(userFrom=current_user, userTo=user, similarity=user_similarity)

        # Perform validation for DB fields
        try:
            new_user_similarities.full_clean()
        except ValidationError, e:
            return "ComputeSimilarity.Failed"

        # Commit to database
        new_user_similarities.save()

    return "ComputeSimilarity.Successful"


def getRelatedness (query1, query2, showVectors=None):

    #Applying FILTERS
    # LowerCase Filter: Set all letters in the string to lower case
    query1 = query1.lower()
    query2 = query2.lower()

    # Tokenizer filter
    tokenizer = re.compile("[' ,]")
    query1_set = tokenizer.split(query1)
    query2_set = tokenizer.split(query2)

    # Length filter, StopWord filter, 3 x PorterStemmer
    # Query 1
    i = 0
    while i < len(query1_set) :
        if query1_set[i] in ENGLISH_STOP_WORDS or len(query1_set[i]) < 3 or len(query1_set[i]) > 100:
            del query1_set[i]
        else:
            query1_set[i] = STEMMER_PORTER.stem_word(STEMMER_PORTER.stem_word(STEMMER_PORTER.stem_word(query1_set[i])))
            i += 1

    #Query 2
    i = 0
    while i < len(query2_set) :
        if query2_set[i] in ENGLISH_STOP_WORDS or len(query2_set[i]) < 3 or len(query2_set[i]) > 100:
            del query2_set[i]
        else:
            query2_set[i] = STEMMER_PORTER.stem_word(STEMMER_PORTER.stem_word(STEMMER_PORTER.stem_word(query2_set[i])))
            i += 1

    # Get the concept vectors
    conceptVector_1 = getConceptVector(query1_set, showVectors)
    conceptVector_2 = getConceptVector(query2_set, showVectors)

    #test is empty concept vector
    if len(conceptVector_1) == 0 or len(conceptVector_2) ==0 :
        return -1

    # Compute cosine similartiy between vectors
    return getCosineSimilarity(conceptVector_1, conceptVector_2)


def getCosineSimilarity(v1,v2):
    dot_product = 0
    norm1 = 0
    norm2 = 0
    print
    for key in v1:
        if key in v2:
            dot_product += v1[key] * v2[key]
        norm1 += math.pow(v1[key], 2)
    for key in v2:
        norm2 += math.pow(v2[key], 2)

    cosine_norm = math.sqrt(norm1) * math.sqrt(norm2)
    if dot_product == 0 or cosine_norm == 0 :
        return 0.0
    else:
        return dot_product / cosine_norm



def getConceptVector(tagSet, showVectors=None) :
    db = MySQLdb.connect(host=config.DATABASES['default']['HOST'], # your host, usually localhost
                         user=config.DATABASES['default']['USER'], # your username
                          passwd=config.DATABASES['default']['PASSWORD'], # your password
                          db=config.DATABASES['default']['NAME']) # name of the data base
    print "---> Database connection established."

    cr = db.cursor()

    concept_vectors = {}
    concept_vectors_sorted = {}

    for term in tagSet:
        print "---> Getting concept vector for term: " + term
        cr.execute("SELECT vector FROM idx WHERE term=%s", term)
        conceptVector_blob = cr.fetchone()

        if conceptVector_blob is None:
            continue

        conceptVector_byteArray = array.array('B',conceptVector_blob[0])
        conceptVector_length = struct.unpack('>I', conceptVector_byteArray[:4]).__getitem__(0)

        print "---> Concept Vector length: " + str(conceptVector_length)

        for i in range(conceptVector_length) :
            current_pos = i * 8 + 4

            concept_id = struct.unpack('>I', conceptVector_byteArray[current_pos:(current_pos + 4)]).__getitem__(0)
            concept_weight = struct.unpack('>f', conceptVector_byteArray[(current_pos + 4):(current_pos + 8)]).__getitem__(0)

            if concept_id in concept_vectors:
                concept_vectors[concept_id] += concept_weight
            else:
                concept_vectors[concept_id] = concept_weight

            if (showVectors == 'y'):# and (i < 10):
                cr.execute("SELECT title FROM articles WHERE id=%s", concept_id)
                concept_title = cr.fetchone()
                print "\tconcept: " + concept_title[0]
                print "\tweight:" + str(concept_weight)
                print "----------"


        # Sort the elements of the conceptVector in descending order by the weight
        #concept_vectors_sorted = sorted(concept_vectors.iteritems(), key=operator.itemgetter(1))
        #concept_vectors_sorted.reverse()

    #normalizeaza fiecare weight la / len(tagSet)

    cr.close()
    db.close()

    return concept_vectors

#print "SEMANTIC RELATEDNESS: " + str(getRelatedness("computer's above science, Programming Languages, Javascript", "Artificial intelligence, Natural language Processing, Semantic Analysis"))


if __name__=="__main__":
    query1 = raw_input("Enter first query: ")
    query2 = raw_input("Enter second query: ")
    show_vectors = raw_input("Show concept vectors (y/*): ")
    print  "SEMANTIC RELATEDNESS: " + str(getRelatedness(query1, query2, show_vectors))