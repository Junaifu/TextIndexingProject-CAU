import os
import json
import sys
import matplotlib.pyplot as plt
import operator

import numpy as np

STOPWORD_FILENAME = "stopWordEnglish.txt"
SCRIPT_DIR = "scripts_Tony"

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
            movieByWriter[writer.split(".")[0]].append(title)
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

def drawPlotForTwoGenre(firstDataDict, secondDataDict):
    plt.figure(figsize=(13, 5))
    plt.subplot(1, 2, 1)
    bars = plt.bar(list(firstDataDict.keys()), list(firstDataDict.values()))
    for bar in bars:
        yVal = bar.get_height()
        plt.text(bar.get_x() + 0.05, yVal + 5, yVal)
    plt.xlabel("Words")
    plt.ylabel("Amount")
    
    plt.subplot(1, 2, 2)
    bars = plt.bar(list(secondDataDict.keys()), list(secondDataDict.values()))
    for bar in bars:
        yVal = bar.get_height()
        plt.text(bar.get_x() + 0.05, yVal + 5, yVal)
    plt.xlabel("Words")
    plt.ylabel("Amount")
    plt.show()

def textIndexingTwoGenre(genres, writers, movieByGenre, movieByWriter, stopWordList):
    userInput = input("Please enter two valid genres, example: Comedy,Romance\n> ")
    if ("," not in userInput):
        printColor(clr.ERROR, "Error commad not valid, redirect to menu")
        askUser(genres, writers, movieByGenre, movieByWriter, stopWordList)
    firstGenre, secondGenre = userInput.lower().split(",")
    if (firstGenre not in genres or secondGenre not in genres):
        printColor(clr.ERROR, "Error one of the genre doesn't exist, redirect to menu")
        askUser(genres, writers, movieByGenre, movieByWriter, stopWordList)

    firstGenreMovieList = movieByGenre[firstGenre]
    secondGenreMovieList = movieByGenre[secondGenre]
    
    printColor(clr.OKBLUE, "Amount of %s: %d" % (firstGenre, len(firstGenreMovieList)))
    printColor(clr.OKBLUE, "Amount of %s: %d" % (secondGenre, len(secondGenreMovieList)))

    firstGenreWordIndexDict = getTextIndexingDict(firstGenreMovieList)
    secondGenreWordIndexDict = getTextIndexingDict(secondGenreMovieList)
   
    # NOTE: Filter Indexing
    filteredFirstGenreWordIndexDict = {word: amount for word, amount in firstGenreWordIndexDict.items() if amount > 100}
    filteredSecondGenreWordIndexDict = {word: amount for word, amount in secondGenreWordIndexDict.items() if amount > 100}
    printColor(clr.OKCYAN, "Total words of the first genre: %d" % sum(filteredFirstGenreWordIndexDict.values()))
    printColor(clr.OKCYAN, "Total words of the second genre: %d" % sum(filteredSecondGenreWordIndexDict.values()))

    # Get Top 10
    filteredFirstGenreWordIndexDict = dict(sorted(firstGenreWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:10])
    filteredSecondGenreWordIndexDict = dict(sorted(secondGenreWordIndexDict.items(), key=operator.itemgetter(1), reverse=True)[:10])

    # NOTE: Draw Charts
    drawPlotForTwoGenre(filteredFirstGenreWordIndexDict, filteredSecondGenreWordIndexDict)


def askUser(genres, writers, movieByGenre, movieByWriter, stopWordList):
    userInput = input(
        """Menu:
                - 1: List genres
                - 2: List Movie by genre
                - 3: List writers
                - 4: List Movie by writer
                - 5: Show stop words
                - 6: TextIndexing between two genres
                - 0: Exit\n> """)
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
        textIndexingTwoGenre(genres, writers, movieByGenre, movieByWriter, stopWordList)
    elif (userInput == '0'):
        sys.exit("Bye.")
    else:
        printColor(clr.ERROR, "Error, try again")
        askUser(genres, writers, movieByGenre, movieByWriter, stopWordList)

if __name__ == "__main__":
    try:
        stopWordFile = open(STOPWORD_FILENAME, "r")
        stopWordList = stopWordFile.read().lower().split("\n")
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
    
    askUser(genres, writers, movieByGenre, movieByWriter, stopWordList)
    
    

    