# This project is an assignment for the module "Natural Language Programming" from ChungAng University 
We can see this project split into 2 parts:
- The scraper
- The "Text Indexing Project"
## Scraper (myScraper.py)

This file contains python code to download (and clean) all on the website [http://www.imsdb.com](http://www.imsdb.com).
The files name will the following: `title@Genres@Writers.txt`
For instance: `Interstellar.html@Adventure,Drama,Sci-Fi@Jonathan Nolan.txt`

This file is originally from https://github.com/j2kun/imsdb_download_all_scripts.
Then I updated the file to my convenience.


#### Create a virtual env:
- Linux: ```virtualenv venv && source venv/bin/activate```
- Windows: ```python -m venv path/to/venv && path/to/venv/Scripts/activate.ps1```
    (If ExecutionPolicy is restricted do this before: Set-ExecutionPolicy Unrestricted -Scope Process)
#### Install dependencies in virtualenv
```
pip install -r requirements.txt
```
#### Launch the download of the files
```
python myScraperIMDB.py
```
Takes about 15 minutes, downloads about 1,100 scripts.

## "Text Indexing Project"
This part is a console application.
Stay in the virtual env with the dependencies and use this command.
```bat
python myTextIndexing.py
```

## Troubleshooting
If there an error with 'collections.Callable' in the bs4/element.py dependency try to update it to 'collections.abc.Callable' (This errors occurs for Windows OS)

## Subject
In this "Text Indexing Project", you have to test the following hypothesis.
Hypothesis: Depending on the features (e.g., genres, directors, cultures, and so on) of movies, the word distribution is statistically different. For example, the words in "Christopher Nolan" movies are different from those in "James Cameron".

0) Design your assumptions. 
1) Choose movie scripts (at least 100?) from https://www.imsdb.com/Links to an external site.
    (I suggest to firstly make each of them in TXT files.)
2) Write a code for indexing the texts, and draw charts for showing the word distributions of them. 
    * Please remove the stop words. (https://en.wikipedia.org/wiki/Stop_words (Links to an external site.)Links to an external site.)
    * NOT allowed to use ANY external libraries (sources).
    * If you find some useful information, please clearly put it in the reference of your slide. 
3) Prepare your slide (PPT) and video (max. 5 minutes). 
4) Submit the zipped file (your code, slide, and video) by Uploading the zipped file to this system no later than Mar 23rd (11:00 AM)
   
* You can use any of programming languages (e.g., Python, Java, and C).
* If you cheat and misconduct, you will automatically fail this course.