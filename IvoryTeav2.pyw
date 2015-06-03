

import sys
import glob
import os
from PyQt4.QtCore import *
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4.Qsci import QsciScintilla, QsciLexerPython
from Main_rc import *


class IvoryTeaUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(IvoryTeaUI, self).__init__()
        self.initUI()
        
            
    def initUI(self):
        # Define widgets
        uic.loadUi("main.ui", self)
        self.splitter.setSizes([300,700])

        # Define Signals and Slots
        self.connect(self.noteList, SIGNAL("currentItemChanged(QListWidgetItem *, QListWidgetItem *)"), self.loadNoteText)
        self.connect(self.settingsButton, SIGNAL("clicked(bool)"), self.loadSettingsDialog)
        
        # Define window geometry
        self.setGeometry(100,100, 1000, 700)
        self.setWindowTitle('Ivory Tea')
    
        # Define Font
        self.fontSelected = QtGui.QFont("Tahoma", 10)
        self.fontSelected.setFixedPitch(True)
        # font metrics here will help building the margin width
        fm = QtGui.QFontMetrics(self.fontSelected)
        
        # QSciScintilla settings
        self.noteText.setFont(self.fontSelected)
        self.noteText.setMarginType(0,QsciScintilla.NumberMargin)
        self.noteText.setMarginsFont(self.fontSelected)
        self.noteText.setMarginWidth(0, fm.width("0000") + 5)
        self.noteText.setMarginLineNumbers(0, True)
        self.noteText.setAutoIndent(True)
        self.noteText.setIndentationGuides(True)
       
        self.buildNoteDict()
        self.loadNoteList()
        
        

    def buildNoteDict(self):
        """
        Notes live here
         Current Assumptions
           1. No subdirectories
           2. Tags to be stored in each file with the special format #TeaTags:<csv seperated tags>
        
        Access variables will be defined for the noteDict data structure.
        
        The structure of the dictionary should be as follows -
        { "filename" : [   "Note Title(currently basename)", "Note Text" ] }
        """
        
        # TODO : Change hardcoding of path to the notes directory.
        self.noteDirectory = 'PATH_TO_NOTES'
        
        # Build a dictionary with Note titles and Note contents.
        self.fileList = [ f for f in os.listdir(self.noteDirectory) if os.path.isfile(os.path.join(self.noteDirectory, f)) ]
        
        # Define Access variables for the noteDict data structure.
        self.NOTE_TITLE=0
        self.NOTE_TEXT=1
        
        # Zero out noteDict
        self.noteDict = {}
        for f in self.fileList:
            self.noteDict[f] = [ os.path.basename(f), open(os.path.join(self.noteDirectory, f), 'r+').read() ]
        
    
    def loadNoteText(self):
        if str(self.noteList.currentItem()) == "None":
            self.noteText.setText("Welcome to Ivory Tea!")
        else:
            self.noteText.setText(self.retrieveNoteText(str(self.noteList.currentItem().text())))
            
    
    def loadNoteList(self):
        self.noteList.addItems(self.retrieveNoteTitles())
        #if str(self.notesList.currentItem()) != 'None':
        self.noteText.setText("Welcome to Ivory Tea!")

        
    def loadSettingsDialog(self):
        self.fontSelected = QtGui.QFontDialog.getFont(self.fontSelected, self);
        self.noteList.setFont(fontSelected[0])
        self.noteText.setFont(fontSelected[0])
        

    # NoteDict helper functions
    def retrieveNoteTitles(self):
        return [ f[0] for f in self.noteDict.values() ]
        
    def retrieveNoteText(self, title):
        return self.noteDict[title][1]
    
def main():
    app = QtGui.QApplication(sys.argv)
    itui = IvoryTeaUI()
    itui.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()        