from tkinter import *
from overusedWords import *

class WordUI(Frame):
    
    #all booleans cover the currrent state of the program (what the player is clicking on)
    def __init__(self, master):
        self.getFile = True
        self.remove = False
        self.add = False
        self.wordAmount = False
        self.multiOpt = False
        self.moreInfo = False
        self.wordChecker = OverusedWords()
        """Initialize the Frame"""
        Frame.__init__(self, master)
        self.master = master
        self.grid()
        self.create_widgets()
    
    
    
    def create_widgets(self):
        """Create button, text, and entry widgets"""
        self.instruction = Label(self, text = "Enter a document to read here (.docx or .txt)")
        self.instruction.grid(row = 0, column = 0, columnspan = 2, sticky = W)
        
        self.entry = Entry(self)
        self.entry.configure(width=80)
        self.entry.grid(row = 1, column = 0, sticky = W)
        
        self.submit_button = Button(self, text = "Submit", command = self.getInput)
        self.submit_button.grid(row = 2, column = 0, sticky = W)
        
        self.text = Text(self, width = 100, height = 30, wrap = WORD)
        self.text.configure(state="disabled")
        
        scroll = Scrollbar(self.master)
        scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)
        
        self.text.grid(row = 3, column = 0, columnspan = 2, sticky = W)
        scroll.grid(column=1, row=0, sticky='NS')
        
        
        
    #accepts a user's click when they put in submit button
    def getInput(self):
        textFile = ""
        
        if self.getFile:
            self.FileInput()
            
        elif self.remove:
            self.wordChecker.newRemove = self.entry.get()
            self.reconfigText("")
            self.instruction["text"] = "Select words you would like added back to the Checker"
            self.remove = False
            self.add = True
            
        elif self.add:
            self.wordChecker.newAdd = self.entry.get()
            self.wordChecker.remove_and_add()
            self.reconfigText("")
            self.instruction["text"] = "Select the max number of overused words you'd like to see"
            self.add = False
            self.wordAmount = True
            
        elif self.wordAmount:
            userInt = self.entry.get()
            if userInt.isdigit():
                self.outputResults(userInt)
                
        elif self.multiOpt:
            self.handleOptions()
        
        elif self.moreInfo:
            self.giveInfo()  
            
                
        
##            
##    


    
    #shows every time a word appeared in its sentence
    def giveInfo(self):
        word = self.entry.get()
        if self.wordChecker.word_appears(word):
            self.text.configure(state="normal")
            self.text.delete(0.0, END)
            self.printInfo(word)
            self.text.configure(state="disabled")
            self.entry.delete(0, END)
            self.moreInfo = False
            self.multiOpt = True
            newFile = "Type 'r' to select a new file, "
            repeatFile = "type 'b' to repeat previous steps on same file, "
            moreInfo = "type 'i' for more word info"
            fullStr = newFile + repeatFile + moreInfo
            self.instruction["text"] = fullStr
            
            
    #prints each time a word appeared in its sentence in bold (helper for giveInfo)
    def printInfo(self, word):
        wordInfo = self.wordChecker.all_word_count[word]
        sentences = self.wordChecker.sentenceList
        self.text.tag_configure("bold", font="Helvetica 12 bold")
        for ind in wordInfo.sentInd:
            sentence = sentences[ind]
            for word in sentence.split(" "):
                if word.lower() == wordInfo.word:
                    self.text.insert("end", word + " ", "bold")
                else:
                    self.text.insert("end", word + " ")
            self.text.insert("end", " \n \n")
        self.text.configure(state="disabled")
        
    
    
    #responds to user choice to restart, go back, or get more info
    def handleOptions(self):
        input = self.entry.get()
        if input == "r":
            self.multiOpt = False
            self.getFile = True
            self.text.configure(state="normal")
            self.text.delete(0.0, END)
            self.text.configure(state="disabled")
            self.wordChecker = OverusedWords()
            self.instruction["text"] = "Enter a document to read here (.docx or .txt)"
            self.entry.delete(0, END)
        elif input == "b":
            self.multiOpt = False
            self.remove = True
            self.instruction["text"] = "Select words you would like removed from the checker"
            self.text.configure(state="normal")
            self.text.delete(0.0, END)
            self.text.insert(0.0, "These words are currently removed from the checker: " + str(self.wordChecker.remove_these_words))
            self.text.configure(state="disabled")
            self.entry.delete(0, END)
        elif input == "i":
            self.multiOpt = False
            self.moreInfo = True
            self.instruction["text"] = "Select a word"
            self.entry.delete(0, END)
            
    
    #prints the total number of most overused words the user wants to see
    def outputResults(self, userInt):
        self.wordChecker.wordCount = int(userInt)
        self.wordChecker.removed_word_count = self.wordChecker.removeWords()
        self.wordChecker.overusedToPrint = self.wordChecker.most_used_words()
        self.wordChecker.wordOverusedStr()
                
        self.text.configure(state="normal")
        self.text.delete(0.0, END)
        self.text.insert(0.0, self.wordChecker.printStr)
        self.text.configure(state="disabled")
                
        newFile = "Type 'r' to select a new file, "
        repeatFile = "type 'b' to repeat previous steps on same file, "
        moreInfo = "type 'i' for more word info"
        fullStr = newFile + repeatFile + moreInfo
        self.instruction["text"] = fullStr
        self.wordAmount = False
        self.multiOpt = True
        self.entry.delete(0, END)
        
    
    #resets the textbox and entry box to empty (can also put newText in the entry box)     
    def reconfigText(self, newText):
        self.entry.delete(0, END)
        self.text.configure(state="normal")
        self.text.delete(0.0, END)
        self.text.insert(0.0, newText)
        self.text.configure(state="disabled")
         
     
    #accept a file that is input if the file is appropriate or print an error message and reprompt user
    #if the file cannot be used
    def FileInput(self):
        input = self.entry.get()
        temp = self.wordChecker.openFile(input)
        success = temp[0]
        
        if success:
            
            self.wordChecker.text = temp[1]
            self.wordChecker.sentenceList = self.wordChecker.make_sentence_list(self.wordChecker.text)
            senList = self.wordChecker.sentenceList
            self.wordChecker.all_word_count = self.wordChecker.save_words(senList)
            
            message = "That is a valid file, please enter your next command"
            self.instruction["text"] = "Select words you would like removed from the checker"
            self.entry.delete(0, END)
            self.text.configure(state="normal")
            self.text.delete(0.0, END)
            self.text.insert(0.0, message)
            self.text.configure(state="disabled")
            
            self.getFile = False
            self.remove = True
            
        else:
            
            errorMess = temp[1]
            self.text.configure(state="normal")
            self.text.delete(0.0, END)
            self.text.insert(0.0, errorMess)
            self.text.configure(state="disabled")
            

root = Tk()
root.resizable(width=False, height=False)
root.grid_columnconfigure(0, weight=1)
root.title("Word Checker")
app = WordUI(root)


root.mainloop()