import os
import json
import sys
import matplotlib.pyplot as plt
import operator
import shlex

STOPWORD_FILENAME = "stopWordEnglish.txt"
SCRIPT_DIR = "scripts"

class clr:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def printColor(color, message):
    if isinstance(message, dict):
        print(color)
        print(message)
        print(clr.ENDC)
        return
    if isinstance(message, list):
        message = ', '.join(message)
    myPrint = print(color + message + clr.ENDC)

def getWordsFormatted(query):
    wordsFiltered = shlex.split(query.replace("and", "").replace("or", ""))
    # wordsFiltered = [word.replace("\"", "") for word in wordsFiltered if word]
    wordsFormatted = []
    for i in range (0, len(wordsFiltered)):
        if (i >= len(wordsFiltered)):
            break
        if (wordsFiltered[i] == "not"):
            wordsFormatted.append(wordsFiltered[i] + " " + wordsFiltered[i + 1])
            wordsFiltered.remove(wordsFiltered[i + 1])
            i += 1
        else:
            wordsFormatted.append(wordsFiltered[i])
    return wordsFormatted

def retrieveGenresAndWriters(files):
    genres = []
    writers = []
    for f in files:
        genresOfMovie = f.split("@")[1].split(",")
        writersOfMovie = f.split("@")[2].split(",")
        writersOfMovie = [writer.split(".")[0] for writer in writersOfMovie]
        genres = list(set(genresOfMovie) | set(genres))
        writers = list(set(writersOfMovie)| set(writers))
    genres.remove('')
    genres = [genre for genre in genres if ' ' not in genre]
    genres = [genre.lower() for genre in genres]
    writers = [writer.lower() for writer in writers]
    writers.sort()
    return genres, writers

def getMoviesByGenre(files, listOfGenre):
    movieByGenre = {k: [] for k in listOfGenre}
    # fileNameByGenre = {k: [] for k in listOfGenre}
    for f in files:
        title, genres, _ = f.split("@")
        for genre in genres.split(","):
            genre = genre.lower().strip()
            if genre == '':
                continue
            movieByGenre[genre].append(f)
            # fileNameByGenre[genre].append(f)
    return movieByGenre

def getMoviesByWriter(files, listOfWriters):
    movieByWriter = {k: [] for k in listOfWriters}
    for f in files:
        title, _, writers = f.split("@")
        for writer in writers.split(","):
            writer = writer.lower()
            movieByWriter[writer.split(".")[0]].append(f)
    return movieByWriter

def getTextIndexingDict(fileNameList):
    wordIndexDict = dict()

    for fileName in fileNameList:
        f = open(SCRIPT_DIR+"/"+fileName, "r", encoding="utf-8");
        corpus = f.read()
        for word in corpus.lower().replace(".", "").replace(",", "").replace("-", "") \
        .replace("*", "").replace("+", "").replace("&", "") \
        .strip().split():
            if word not in stopWordList:
                if word not in wordIndexDict:
                    wordIndexDict[word] = 0
                wordIndexDict[word] += 1
    return wordIndexDict

def drawPlotForTwoGenre(firstDataDict, secondDataDict, firstGenre, secondGenre, isPercent=False, ylabel="Amount", xlabel="Words"):
    plt.figure(figsize=(13, 6.5))
    plt.subplot(1, 2, 1)
    firstDataValueList = list(firstDataDict.values())
    bars = plt.bar(list(firstDataDict.keys()), firstDataValueList)
    if isPercent == True:
        for i in range(len(bars)):
            plt.text(i, firstDataValueList[i], str(firstDataValueList[i]) + "%", rotation=30, ha='center')
    else:
        for i in range(len(bars)):
            plt.text(i, firstDataValueList[i], firstDataValueList[i], rotation=30, ha='center')        
    plt.title(firstGenre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=60)
    
    plt.subplot(1, 2, 2)
    firstDataValueList = list(secondDataDict.values())
    bars = plt.bar(list(secondDataDict.keys()), firstDataValueList)
    if isPercent == True:        
        for i in range(len(bars)):
            plt.text(i, firstDataValueList[i], str(firstDataValueList[i]) + "%", rotation=30, ha='center')
    else:
        for i in range(len(bars)):
            plt.text(i, firstDataValueList[i], firstDataValueList[i], rotation=30, ha='center')        
    plt.title(secondGenre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=60)
    
    plt.show()

def menuTwoGenre(firstGenreWordIndexDict, secondGenreWordIndexDict, firstGenre, secondGenre):
    userInput = input("""Options:
                1 - Plot bar with the N most used words from the two genres
                2 - Plot bar with the frequency of the N most used words from the two genres
                0 - Go back to menu
                      \n> """)
   
    if (userInput == "1"):
        try:
            n = int(input(clr.OKCYAN + "Enter the number of max words to display in charts (Default: 10)\n> " + clr.ENDC))
        except:
            n = 10
        filteredFirstGenreWordIndexDict = dict(sorted(firstGenreWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:n])
        filteredSecondGenreWordIndexDict = dict(sorted(secondGenreWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:n])

        printColor(clr.OKBLUE, "Total words in among the %d most used word from the first genre: %d" % (n, sum(filteredFirstGenreWordIndexDict.values())))
        printColor(clr.OKBLUE, "Total words in among the %d most used word from the second genre: %d" % (n, sum(filteredSecondGenreWordIndexDict.values())))
        drawPlotForTwoGenre(filteredFirstGenreWordIndexDict, filteredSecondGenreWordIndexDict, firstGenre, secondGenre)
    elif (userInput == "2"):
        try:
            n = int(input(clr.OKCYAN + "Enter the number of max words to display in charts (Default: 10)\n> " + clr.ENDC))
        except:
            n = 10
        firstGenreTotalWords = sum(firstGenreWordIndexDict.values())
        secondGenreTotalWords = sum(secondGenreWordIndexDict.values())
        totalWords = secondGenreTotalWords + firstGenreTotalWords;
        printColor(clr.OKBLUE, "Total words of the first genre: %d" % firstGenreTotalWords)
        printColor(clr.OKBLUE, "Total words of the second genre: %d" % secondGenreTotalWords)
        printColor(clr.OKBLUE, "Total words: %d" % totalWords)
        filteredFirstGenreWordIndexDict = dict(sorted(firstGenreWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:n])
        filteredSecondGenreWordIndexDict = dict(sorted(secondGenreWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:n])
        
        filteredFirstGenreWordIndexDict = {word: round((int(amount)/totalWords) * 100, 2) for word, amount in filteredFirstGenreWordIndexDict.items()}
        filteredSecondGenreWordIndexDict = {word: round((int(amount)/totalWords) * 100, 2) for word, amount in filteredSecondGenreWordIndexDict.items()}
        drawPlotForTwoGenre(filteredFirstGenreWordIndexDict, filteredSecondGenreWordIndexDict, firstGenre, secondGenre, True, "frequency")
        
    elif (userInput == "0"):
        return
    menuTwoGenre(firstGenreWordIndexDict, secondGenreWordIndexDict, firstGenre, secondGenre)

def textIndexingTwoGenres(genres, movieByGenre, stopWordList):
    userInput = input(clr.OKCYAN + "Please enter two valid genres, example: Comedy,Romance\n> " + clr.ENDC)
    if ("," not in userInput):
        printColor(clr.ERROR, "Error command not valid, redirect to menu")
        return
    firstGenre, secondGenre = userInput.lower().split(",")
    if (firstGenre not in genres or secondGenre not in genres):
        printColor(clr.ERROR, "Error one of the genre doesn't exist, redirect to menu")
        return

    firstGenreMovieList = movieByGenre[firstGenre]
    secondGenreMovieList = movieByGenre[secondGenre]
    
    printColor(clr.OKBLUE, "Amount of %s movies: %d" % (firstGenre, len(firstGenreMovieList)))
    printColor(clr.OKBLUE, "Amount of %s movies: %d" % (secondGenre, len(secondGenreMovieList)))

    firstGenreWordIndexDict = getTextIndexingDict(firstGenreMovieList)
    secondGenreWordIndexDict = getTextIndexingDict(secondGenreMovieList)
   
    menuTwoGenre(firstGenreWordIndexDict, secondGenreWordIndexDict, firstGenre, secondGenre)

def menuTwoWriter(firstWriterWordIndexDict, secondWriterWordIndexDict, firstWriter, secondWriter):
    userInput = input("""Options:
                1 - Plot bar with the N most used words from the two writers
                2 - Plot bar with the frequency of the N most used words from the two writers
                0 - Go back to menu
                      \n> """)
   
    if (userInput == "1"):
        try:
            n = int(input(clr.OKCYAN + "Enter the number of max words to display in charts (Default: 10)\n> " + clr.ENDC))
        except:
            n = 10
        filteredFirstWriterWordIndexDict = dict(sorted(firstWriterWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:n])
        filteredSecondWriterWordIndexDict = dict(sorted(secondWriterWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:n])

        printColor(clr.OKBLUE, "Total words in among the %d most used word from the first writer: %d" % (n, sum(filteredFirstWriterWordIndexDict.values())))
        printColor(clr.OKBLUE, "Total words in among the %d most used word from the second writer: %d" % (n, sum(filteredSecondWriterWordIndexDict.values())))
        drawPlotForTwoGenre(filteredFirstWriterWordIndexDict, filteredSecondWriterWordIndexDict, firstWriter, secondWriter)
    elif (userInput == "2"):
        try:
            n = int(input(clr.OKCYAN + "Enter the number of max words to display in charts (Default: 10)\n> " + clr.ENDC))
        except:
            n = 10
        firstWriterTotalWords = sum(firstWriterWordIndexDict.values())
        secondWriterTotalWords = sum(secondWriterWordIndexDict.values())
        totalWords = secondWriterTotalWords + firstWriterTotalWords;
        printColor(clr.OKBLUE, "Total words of the first writer: %d" % firstWriterTotalWords)
        printColor(clr.OKBLUE, "Total words of the second writer: %d" % secondWriterTotalWords)
        printColor(clr.OKBLUE, "Total words: %d" % totalWords)
        filteredFirstWriterWordIndexDict = dict(sorted(firstWriterWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:n])
        filteredSecondWriterWordIndexDict = dict(sorted(secondWriterWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:n])
        
        filteredFirstWriterWordIndexDict = {word: round((int(amount)/totalWords) * 100, 2) for word, amount in filteredFirstWriterWordIndexDict.items()}
        filteredSecondWriterWordIndexDict = {word: round((int(amount)/totalWords) * 100, 2) for word, amount in filteredSecondWriterWordIndexDict.items()}
        drawPlotForTwoGenre(filteredFirstWriterWordIndexDict, filteredSecondWriterWordIndexDict, firstWriter, secondWriter, True, "Frequency")
        
    elif (userInput == "0"):
        return
    menuTwoWriter(firstWriterWordIndexDict, secondWriterWordIndexDict, firstWriter, secondWriter)

def textIndexingTwoWriters(writers, movieByWriters, stopWordList):
    userInput = input(clr.OKCYAN + "Please enter two valid writers, example: Christopher Nolan,James Cameron\n> " + clr.ENDC)
    if ("," not in userInput):
        printColor(clr.ERROR, "Error command not valid, redirect to menu")
        return
    firstWriter, secondWriter = userInput.lower().split(",")
    if (firstWriter not in writers or secondWriter not in writers):
        printColor(clr.ERROR, "Error one of the writer doesn't exist, redirect to menu")
        return

    firstWriterMovieList = movieByWriter[firstWriter]
    secondWriterMovieList = movieByWriter[secondWriter]
    
    printColor(clr.OKBLUE, "Amount of movies writen by %s: %d" % (firstWriter, len(firstWriterMovieList)))
    printColor(clr.OKBLUE, "Amount of movies writen by %s: %d" % (secondWriter, len(secondWriterMovieList)))

    firstWriterWordIndexDict = getTextIndexingDict(firstWriterMovieList)
    secondWriterWordIndexDict = getTextIndexingDict(secondWriterMovieList)
   
    menuTwoWriter(firstWriterWordIndexDict, secondWriterWordIndexDict, firstWriter, secondWriter)

def selectGenreForMenu(genres, movieByGenre, stopWordList):
    userInput = input("Enter a genre of movie for the model (enter \"list\" to display the list of genre):")
    if (userInput == "list"):
        printColor(clr.OKGREEN, genres)
        selectGenreForMenu(genres, movieByGenre, stopWordList)
        return
    elif (userInput not in genres):
        printColor(clr.ERROR, "This genre doesn't exist")
        selectGenreForMenu(genres, movieByGenre, stopWordList)
        return
    printColor(clr.OKBLUE, "Number of movie [" + userInput + "]: " + str(len(movieByGenre[userInput])))
    modelsMenu(userInput, movieByGenre, stopWordList)

def computeAndShowRevelentBooleanModelResult(queryConditionDict, moviesName, wordsFormatted, userQuery):
    queries = [query.strip() for query in userQuery.split("or")]
    retrievedMovie = []
    for movie in moviesName:
        for query in queries:
            andQueries = [q.strip() for q in query.split("and")]
            isQueryTrue = queryConditionDict[andQueries[0]][movie]
            for word in andQueries:
                isQueryTrue = isQueryTrue & queryConditionDict[word][movie]
            if isQueryTrue:
                retrievedMovie.append(movie)
    if (len(retrievedMovie) == 0):
        printColor(clr.WARNING, "There are no revelent movies")
        return
    maxLengthMovieName = len(max(retrievedMovie, key=len))
    print("Boolean Model Revelent Result:\n")
    print("Movie Name".ljust(maxLengthMovieName), end="\t")
    for word in wordsFormatted:
            print(word, end="\t")
    print("")
    for movie in retrievedMovie:
        print(movie.ljust(maxLengthMovieName), end="\t")
        for word in wordsFormatted:
            print(str(queryConditionDict[word][movie]).ljust(len(word)), end="\t")
        print("")
    return retrievedMovie


def booleanModelResultMenu(queryConditionDict, moviesName, wordsFormatted, query):
    userInput = input("""Options:
                1 - All result
                2 - Revelent result
                0 - Go Back
                          \n> """)
    if (userInput == "1"):
        maxLengthMovieName = len(max(moviesName, key=len))
        print("Boolean Model All Result:\n")
        print("Movie Name".ljust(maxLengthMovieName), end="\t")
        for word in wordsFormatted:
            print(word, end="\t")
        print("")
        for movie in moviesName:
            print(movie.ljust(maxLengthMovieName), end="\t")
            for word in wordsFormatted:
                 print(str(queryConditionDict[word][movie]).ljust(len(word)), end="\t")
            print("")
    elif (userInput == "2"):
        computeAndShowRevelentBooleanModelResult(queryConditionDict, moviesName, wordsFormatted, query)
    elif (userInput == "0"):
        return
    booleanModelResultMenu(queryConditionDict, moviesName, wordsFormatted, query)
    

def doBooleanModel(selectedGenre, isPrecisionAndRecall):
    query = ""
    if not isPrecisionAndRecall:
        query = input("""Enter a query:
            - words
            - 'AND' or 'OR' or 'NOT' keyword (no case-sensitive)
            - Do not use parenthesis, it doesn't work\nExample: <dead and cry and not joy>: """)
        query = query.lower()
        if (query == ""):
            printColor(clr.ERROR, "You need to enter a query")
            doBooleanModel(selectedGenre, False)
            return
        elif ("(" in query or ")" in query):
            printColor(clr.ERROR, "Parenthesis aren't accepted")
            doBooleanModel(selectedGenre, False)
            return
    else:
        query = "mine and explosion and dead"
        printColor(clr.OKBLUE, "Selected genre for precision and recall: " + clr.OKGREEN + selectedGenre + clr.OKBLUE + "\nQuery will be: " + clr.OKGREEN + query + clr.ENDC  + "\nThe word \"mine\" here will refer to \"a type of bomb put below the earth\"")

    movieMatch = []
    selectedGenreFileNameList = movieByGenre[selectedGenre]
    wordsFormatted = getWordsFormatted(query)
    queryConditionDict = {}
    moviesName = []
    for word in wordsFormatted:
        queryConditionDict[word] = {}
    for fileName in selectedGenreFileNameList:
        f = open(SCRIPT_DIR+"/"+fileName, "r", encoding="utf-8");
        corpus = f.read().lower().strip().split()
        movieName = fileName.split("@")[0].split(".html")[0]
        moviesName.append(movieName)
        for word in wordsFormatted:
            queryConditionDict[word][movieName] = word.split(" ")[1] not in corpus if "not" in word else word in corpus
    if not isPrecisionAndRecall:
        booleanModelResultMenu(queryConditionDict, moviesName, wordsFormatted, query)
    else:
        retrievedMovie = len(computeAndShowRevelentBooleanModelResult(queryConditionDict, moviesName, wordsFormatted, query))
        # True Positive
        rightMeaningMineBomb = 6
        # False Positive
        retrievedMovieFalsePositive = retrievedMovie - rightMeaningMineBomb
        print("retrievedMovieFalsePositive: " + str(retrievedMovieFalsePositive))
        # False negative: There are not false negative
        falseNegative = 0
        precision = rightMeaningMineBomb / (rightMeaningMineBomb + retrievedMovieFalsePositive)
        recall = rightMeaningMineBomb / (rightMeaningMineBomb + falseNegative)
        printColor(clr.OKBLUE, "Precision: {0} {1} {2}\nRecall: {3} {4}".format(clr.OKGREEN, precision, clr.OKBLUE, clr.OKGREEN, recall))

    return

def modelsMenu(selectedGenre, movieByGenre, stopWordList):
    userInput = input("""Options:
                1 - Boolean model
                2 - Vector model
                0 - Go back to menu
                          \n> """)
   
    if (userInput == "1"):
        doBooleanModel(selectedGenre, False)
    elif (userInput == "0"):
        return
    modelsMenu(selectedGenre, movieByGenre, stopWordList)

def menu(genres, writers, movieByGenre, movieByWriter, stopWordList):
    userInput = input(
        """Menu:
                1 - List genres
                2 - List Movie by genre
                3 - List writers
                4 - List Movie by writer
                5 - Show stop words
                6 - TextIndexing between two genres
                7 - TextIndexing between two writers
                8 - Models with one genre
                9 - Boolean model precision & recall
                0 - Exit\n> """)
    if (userInput == '1'):
        printColor(clr.OKGREEN, genres)
    elif (userInput == '2'):
        printColor(clr.OKGREEN, movieByGenre)
    elif (userInput == '3'):
        printColor(clr.OKGREEN, writers)
    elif (userInput == '4'):
        printColor(clr.OKGREEN, movieByWriter)
    elif (userInput == '5'):
        printColor(clr.OKBLUE, stopWordList)
    elif (userInput == '6'):
        textIndexingTwoGenres(genres, movieByGenre, stopWordList)
    elif (userInput == '7'):
        textIndexingTwoWriters(writers, movieByWriter, stopWordList)
    elif (userInput == '8'):
        selectGenreForMenu(genres, movieByGenre, stopWordList)
    elif (userInput == '9'):
        doBooleanModel("war", True)
    elif (userInput == '0'):
        sys.exit("Bye.")
    else:
        printColor(clr.ERROR, "Error, try again")
    menu(genres, writers, movieByGenre, movieByWriter, stopWordList)

if __name__ == "__main__":
    try:
        stopWordFile = open(STOPWORD_FILENAME, "r")
        stopWordList = stopWordFile.read().lower().split("\n")
        # NOTE: remove duplicate
        stopWordList = list(dict.fromkeys(stopWordList))
    except:
        printColor(clr.ERROR, STOPWORD_FILENAME + " not found. Please provide a stopword file with this name")
        sys.exit(-1)
    
    files = os.listdir(SCRIPT_DIR)
    movieByGenre = None
    movieByWriter = None
    genres, writers = retrieveGenresAndWriters(files)
    # NOTE: Create a json file for the movieByGenre and movieByWriter
    if (not os.path.exists("MovieByGenre.json")):
        print("Creating the file MovieByGenre...")
        movieByGenre = getMoviesByGenre(files, genres)
        with open('MovieByGenre.json', 'w') as fp:
            json.dump(movieByGenre, fp)
    else:
        f = open("MovieByGenre.json")
        movieByGenre = json.loads(f.read())

    if (not os.path.exists("MovieByWriter.json")):
        print("Creating the file MovieByWriter...")
        movieByWriter = getMoviesByWriter(files, writers)
        with open('MovieByWriter.json', 'w') as fp:
            json.dump(movieByWriter, fp)
    else:
        f = open("MovieByWriter.json")
        movieByWriter = json.loads(f.read())
    menu(genres, writers, movieByGenre, movieByWriter, stopWordList)
    
    

    