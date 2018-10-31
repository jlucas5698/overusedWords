#NOTE: Program requires docx2txt to be downloaded
import docx2txt
import copy
import tkinter
import re
#prompts user for a file, opens it when their input is valid
#otherwise continually prompts user until they pick a valid file
#accepts only .docx (recent Word Files) or .txt files


#saves the index of each sentence the word
#appears in and the total number of times it appears at the index
#in the sentence
#also saves name of word and total appearances
#of word in the file
class Overused:
    def __init__(self, word):
        self.word = word
        self.sentInd = {}
        self.count = 1
    #key: the index of the sentence
    #value: the number of appearances of the word at that index
    

#does all the backend stuff--keeping track of most used words, words to remove, etc
class OverusedWords:
    
    def __init__(self):
        #text -- the opened file
        self.text = ""
        #sentenceList -- the file split apart into sentences
        self.sentenceList = []
        #all_word_count -- dict of all words and how much they're used
        #key: word, val: Overused class
        self.all_word_count = {}
        #newAdd and newRemove are new words to add or remove from the output dict
        #remove_these_words is all words to be removed from the output dict 
        self.newAdd = ""
        self.newRemove = ""
        self.remove_these_words = []
        #wordCount -- # of most overused words the user will see
        self.wordCount = 0
        #removed_word_count--new dict excluding words the user doesn't wnat to see
        self.removed_word_count = {}
        #overusedToPrint -- all words the user will ultimately see, based on wordCount
        self.overusedToPrint = []
        #printStr -- collects whole string of all words that were used adn number of appearances
        #to be printed in the UI
        self.printStr = ""
    
    #returns file type of the file fileName -- either .docx or .txt or unknown
    def fileType(fileName):
        fileType = ""
        fileName = fileName.rstrip() #removes trailing whitespace
        docx = ".docx"
        txt = ".txt"
        if fileName.endswith(docx):
            fileType = docx
        elif fileName.endswith(txt):
            fileType = txt
        else:
            fileType = "unknown"
        return fileType
    
    
    #if the file was opened, returns True and the open contents of the file
    #if the file could not be opened, returns false and the error message
    def openFile (self, fileName):
        try:
            if OverusedWords.fileType(fileName) == ".docx":
                text = docx2txt.process(fileName)
                return True, text
            elif OverusedWords.fileType(fileName) == ".txt":
                tempText = open(fileName, "r")
                text = tempText.read()
                return True, text
            else:
                return False, "that is not a valid file"
        except IOError:
            return False, "Your file could not be found in your current directory.  Please enter a different file name"


    

    #removes anything that isn't a letter from a word string (useful when string contains word followed by comma
    #and we want to count the word, etc)
    def remove_non_letters(word):
        newWord = ""
        for letter in word:
            if letter.isalnum():
                newWord += letter
        return newWord

    
    ##saves words in a dictionary that counts the word usage that is then returned
    def save_words(save, sentences):
        wordDict = {}
        sentenceInd = 0
        for sentence in sentences:
            for word in sentence.split(" "):
                word = OverusedWords.remove_non_letters(word)
                word = word.lower()
                if word != "":
                    wordDict = OverusedWords.add_to_dict(wordDict, word, sentenceInd)
            sentenceInd += 1
        return wordDict


    #takes as input a dict of Overused objects and a word
    #if the word is already in the dict add to the total count of the object
    #otherwise add a new object representing the word to the dict
    def add_to_dict(wordDict, word, index):
        if word in wordDict:
            savedWord = wordDict[word]
            savedWord.count += 1
            if index in savedWord.sentInd:
                savedWord.sentInd[index] += 1
            else:
                savedWord.sentInd[index] = 1
            wordDict[word] = savedWord
        else:
            wordInfo = Overused(word)
            wordInfo.sentInd[index] = 1
            wordDict[word] = wordInfo
        return wordDict
        

    
    #returns a list of the top most-used-words, based on the amoutn the user wants to see
    def most_used_words(self):
        wordDict = self.removed_word_count
        saveNum = self.wordCount
        wordArr = OverusedWords.dict_to_arr(wordDict)
        wordArr = sorted(wordArr, key=lambda Overused: Overused.count, reverse=True)
        mostUsed = []
        for wordObj in wordArr:
            mostUsed.append(wordObj)
            saveNum -= 1
            if saveNum == 0:
                break
        return mostUsed


    #takes as input dictionary of overused words, converts to object array
    def dict_to_arr(wordDict):
        wordArr = []
        for word, wordObj in wordDict.items():
            wordArr.append(wordObj)
        return wordArr
        
            

    #takes as input a word file, returns an array
    #made up of sentences
    def make_sentence_list(self, text):
        sentences = []
        for sentence in re.split('[?.]', text):
            sentences.append(sentence)
        return sentences
        


    #removes any words the user  from the list
    #also adds back any words the user wants added back
    #takes as input list of words the user previously wanted removed
    #allows user to add or remove any words they choose from this list
    #returns the new list
    def remove_and_add(self):
        alreadyRemoved = self.remove_these_words
        self.newRemove = self.newRemove.lower()
        self.newAdd = self.newAdd.lower()
        newRemList = self.newRemove.split(" ")
        newAddList = self.newAdd.split(" ")
        for remove in newRemList:
            if remove not in alreadyRemoved:
                alreadyRemoved.append(remove)
        for add in newAddList:
            if add in alreadyRemoved:
                alreadyRemoved.remove(add)
        self.remove_these_words = alreadyRemoved


    #removes any words the user doesn't want to have checked
    def removeWords(self):
        newDict = copy.deepcopy(self.all_word_count)
        for word in self.remove_these_words:
            if word in newDict:
                del newDict[word]
        return newDict

    
    
    def word_appears(self, word):
        if word in self.all_word_count:
            return True
        return False
        
    
    
    #accepts as input an array of all sentences in text file
    #and an Overused object containing info about each sentence
    #where the word is located
    #adds quotation marks any times the word appears and prints the string
    def save_all_appearances(self, word):
        
        wordInfo = self.all_word_count[word]
        sentences = self.sentenceList
        quoteWordSent = ""
        for ind in wordInfo.sentInd:
            sentence = sentences[ind]
            #print(sentence, "\n")
            for word in sentence.split(" "):
                if word == wordInfo.word:
                    word = BOLD + word + NORMAL
                    quoteWordSent += word + " "
                else:
                    quoteWordSent += word + " "
            quoteWordSent = quoteWordSent + "\n"
        return quoteWordSent + "\n \n"
        
    
    #returns a string containing info about the most overused words that the user would like to see
    def wordOverusedStr(self):
        self.printStr = ""
        for wordInfo in self.overusedToPrint:
            self.printStr = self.printStr + wordInfo.word + ": " + str(wordInfo.count) + "\n"
            self.printStr = self.printStr + "Word appears at these indexes this many times: \n"
            #print_all_appearances(sentenceList, wordInfo)
            for ind, count in wordInfo.sentInd.items():
                self.printStr = self.printStr + str(ind) + ":" + str(count) +  ", "
            self.printStr = self.printStr + "\n \n"
                


