# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
# Created by: PyQt5 UI code generator 5.15.9


from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
import re
import requests
from string import ascii_lowercase
import itertools
import random
import math
import os


class Ui_MainWindow(object):
    # setup the ui
    def setupUi(self, MainWindow):
        # geometry vars
        self.width = 600
        self.height = 500
        self.outerMargin = 15
        self.innerWidth = self.width - 2 * (self.outerMargin)
        self.innerHeight = self.height - 2 * (self.outerMargin)
        self.menuHeight = 23
        self.verticalSpacing = 20
        self.helpTextStyle = """
                color: #5A5A5A;
            """
        self.labelRangeSingle = "E.g.: a-z, a-j, g-z. Default: a-z."
        self.labelRangeDouble = "E.g.: aa-zz, ab-jn, gc-gz. Default: aa-zz."
        # inputs
        self.query = ""
        self.rangeText = ""
        self.cpList = []
        self.searchItems = []
        # request header
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }
        self.proceed = True
        # colors
        self.colors = {"red": "#db203a", "green": "#00994d"}
        # export button labels
        self.exportLabel = {"txt": "Export as TXT", "csv": "Export as CSV"}

        # main window
        self.MainWindow = MainWindow
        self.MainWindow.setFixedSize(self.width, self.height)
        self.MainWindow.setWindowTitle("AutoCollect")
        self.MainWindow.setWindowIcon(QtGui.QIcon("AutoCollect.ico"))

        # central parent widget
        self.centralWidget = QtWidgets.QWidget()

        # grid layout widget
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(
            QtCore.QRect(
                self.outerMargin,
                self.outerMargin,
                self.innerWidth,
                self.innerHeight - self.menuHeight,
            )
        )

        # grid layout
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(self.verticalSpacing)

        # add the components
        self.createMenuBar()
        # self.createStatusBar()
        self.createQuery()
        self.createSize()
        self.createRange()
        self.createCP()
        self.createStartButton()
        self.createStopButton()
        self.createResetButton()
        self.createExportButton()
        self.createDivider()
        self.createProgressBar()
        self.createConsole()

        # add central widget
        self.MainWindow.setCentralWidget(self.centralWidget)

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    # create query component
    def createQuery(self):
        # vertical layout col 1
        vLayout1 = QtWidgets.QVBoxLayout()
        # label
        labelQuery = QtWidgets.QLabel("Query")
        vLayout1.addWidget(labelQuery)
        # empty label for taking space
        emptyLabel = QtWidgets.QLabel()
        vLayout1.addWidget(emptyLabel)
        self.gridLayout.addLayout(vLayout1, 0, 0, 1, 1)
        # vertical layout col 2
        vLayout2 = QtWidgets.QVBoxLayout()
        vLayout2.setSpacing(8)
        # input
        self.lineEditQuery = QtWidgets.QLineEdit()
        vLayout2.addWidget(self.lineEditQuery)
        # help text
        labelQueryHelp = QtWidgets.QLabel(
            "Write the search Query, use [alphabet] for alphabet placeholder"
        )
        labelQueryHelp.setStyleSheet(self.helpTextStyle)
        vLayout2.addWidget(labelQueryHelp)
        self.gridLayout.addLayout(vLayout2, 0, 1, 1, 4)

    # create alphabet-size component
    def createSize(self):
        # label
        labelSize = QtWidgets.QLabel("Alphabet Size")
        self.gridLayout.addWidget(labelSize, 1, 0, 1, 1)
        # radio button single alphabet
        self.radioSingle = QtWidgets.QRadioButton("Single (a, b, ..., z)")
        self.radioSingle.setChecked(True)
        self.radioSingle.toggled.connect(self.radioClicked)
        self.gridLayout.addWidget(self.radioSingle, 1, 1, 1, 1)
        # radio button double alphabets
        self.radioDouble = QtWidgets.QRadioButton("Double (aa, ab, ..., zz)")
        self.radioDouble.toggled.connect(self.radioClicked)
        self.gridLayout.addWidget(self.radioDouble, 1, 2, 1, 1)

    # create alphabet range component
    def createRange(self):
        # label
        labelRange = QtWidgets.QLabel("Alphabet Range")
        self.gridLayout.addWidget(labelRange, 2, 0, 1, 1)
        # input
        self.LineEditRange = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.LineEditRange, 2, 1, 1, 1)
        # help text
        self.labelRangeHelp = QtWidgets.QLabel(self.labelRangeSingle)
        self.labelRangeHelp.setStyleSheet(self.helpTextStyle)
        self.gridLayout.addWidget(self.labelRangeHelp, 2, 2, 1, 3)

    # create cursor position component
    def createCP(self):
        # label
        self.labelCP = QtWidgets.QLabel("Cursor Positions")
        self.gridLayout.addWidget(self.labelCP, 3, 0, 1, 1)
        # input
        self.LineEditCP = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.LineEditCP, 3, 1, 1, 1)
        # help text
        labelCPHelp = QtWidgets.QLabel("E.g.: 2, 7, 10. Default: End of each word")
        labelCPHelp.setStyleSheet(self.helpTextStyle)
        self.gridLayout.addWidget(labelCPHelp, 3, 2, 1, 3)

    # create start button
    def createStartButton(self):
        self.buttonStart = QtWidgets.QPushButton("Start")
        self.buttonStart.clicked.connect(self.startClicked)
        self.gridLayout.addWidget(self.buttonStart, 4, 0, 1, 2)

    # create stop button
    def createStopButton(self):
        self.buttonStop = QtWidgets.QPushButton("Stop")
        self.buttonStop.clicked.connect(self.stopClicked)
        self.buttonStop.setEnabled(False)
        self.gridLayout.addWidget(self.buttonStop, 4, 2, 1, 1)

    # create reset button
    def createResetButton(self):
        self.buttonReset = QtWidgets.QPushButton("Reset")
        self.buttonReset.clicked.connect(self.resetClicked)
        self.gridLayout.addWidget(self.buttonReset, 4, 3, 1, 1)

    # create export button
    def createExportButton(self):
        self.buttonExport = QtWidgets.QPushButton("Export")
        self.buttonExport.clicked.connect(self.exportClicked)
        self.buttonExport.setEnabled(False)
        self.gridLayout.addWidget(self.buttonExport, 4, 4, 1, 1)

    # create divider
    def createDivider(self):
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(divider, 5, 0, 1, 5)

    # create progress bar
    def createProgressBar(self):
        self.progressBar = QtWidgets.QProgressBar()
        self.gridLayout.addWidget(self.progressBar, 6, 0, 1, 5)

    # create console
    def createConsole(self):
        self.textEditConsole = QtWidgets.QTextEdit()
        self.textEditConsole.setReadOnly(True)
        self.gridLayout.addWidget(self.textEditConsole, 7, 0, 1, 5)

    # create status bar
    def createStatusBar(self):
        self.statusbar = QtWidgets.QStatusBar()
        self.MainWindow.setStatusBar(self.statusbar)

    # create menu bar
    def createMenuBar(self):
        # menu bar
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width, self.menuHeight))
        # help menu
        self.menuHelp = QtWidgets.QMenu("Help")
        self.menubar.addAction(self.menuHelp.menuAction())
        # about menu
        self.menuAbout = QtWidgets.QMenu("About")
        self.menubar.addAction(self.menuAbout.menuAction())
        # add menu bar
        self.MainWindow.setMenuBar(self.menubar)

    # radio button on click callback
    def radioClicked(self):
        self.LineEditRange.setText("")
        if self.radioSingle.isChecked():
            self.labelRangeHelp.setText(self.labelRangeSingle)
        if self.radioDouble.isChecked():
            self.labelRangeHelp.setText(self.labelRangeDouble)

    # start button on click callback
    def startClicked(self):
        self.clearErrorBeforeStart()
        self.proceed = True
        queryOkay = self.checkQuery()
        if not queryOkay:
            return
        rangeOkay = self.checkRange()
        if not rangeOkay:
            return
        cpOkay = self.checkCP()
        if not cpOkay:
            return
        # get the search items and show the confirmation dialog
        self.getSearchItems()
        self.confirmFetch()

    # clear console and remove red border before starting
    def clearErrorBeforeStart(self):
        self.textEditConsole.setText("")
        self.lineEditQuery.setStyleSheet("border: 1px solid black;")
        self.LineEditRange.setStyleSheet("border: 1px solid black;")
        self.LineEditCP.setStyleSheet("border: 1px solid black;")

    # check query after clicking start
    # also update the query text
    def checkQuery(self):
        self.query = self.lineEditQuery.text().strip()
        if self.query == "":
            self.logError("Query is empty.", self.lineEditQuery)
            return False
        if "[alphabet]" not in self.query:
            self.logError(
                "Alphabet placeholder [alphabet] missing in query.", self.lineEditQuery
            )
            return False
        self.query = re.sub(r"\s+", " ", self.query)
        return True

    # check range after clicking start
    # also update the range text
    def checkRange(self):
        self.rangeText = self.LineEditRange.text().strip().lower()
        if self.rangeText == "":
            if self.radioSingle.isChecked():
                self.rangeText = "a-z"
                return True
            if self.radioDouble.isChecked():
                self.rangeText = "aa-zz"
                return True
        if self.radioSingle.isChecked():
            match = re.match(r"^[a-z]-[a-z]$", self.rangeText)
            if not match:
                self.logError("Invalid alphabet range.", self.LineEditRange)
                return False
            if ord(self.rangeText[0]) > ord(self.rangeText[2]):
                self.logError("Invalid order in alphabet range.", self.LineEditRange)
                return False
        if self.radioDouble.isChecked():
            match = re.match(r"^[a-z]{2}-[a-z]{2}$", self.rangeText)
            if not match:
                self.logError("Invalid alphabet range.", self.LineEditRange)
                return False
            if ord(self.rangeText[0]) > ord(self.rangeText[3]):
                self.logError("Invalid order in alphabet range1.", self.LineEditRange)
                return False
            if self.rangeText[1] != "z" and (
                ord(self.rangeText[1]) > ord(self.rangeText[4])
            ):
                self.logError("Invalid order in alphabet range2.", self.LineEditRange)
                return False
            if self.rangeText[:2] == "zz":
                self.logError("Invalid order in alphabet range3.", self.LineEditRange)
                return False
        return True

    # check CP after clicking start
    # also update the CP list
    def checkCP(self):
        self.cpList = []
        cp = self.LineEditCP.text().strip()
        if cp != "":
            self.cpList = cp.split(",")
            err = False
            cpListStripped = []
            for x in self.cpList:
                x = x.strip()
                if x == "":
                    err = True
                    break
                match = re.match(r"\D", x)
                if match:
                    err = True
                    break
                cpListStripped.append(x)
            if err:
                self.logError("Invalid cursor positions.", self.LineEditCP)
                return False
            cpListSorted = sorted(cpListStripped)
            if int(cpListSorted[-1]) > len(self.query):
                self.logError(
                    "Cursor position greater than query length.", self.LineEditCP
                )
                return False
            self.cpList = cpListSorted
            return True
        if self.radioSingle.isChecked():
            q = self.query.replace("[alphabet]", "-")
        if self.radioDouble.isChecked():
            q = self.query.replace("[alphabet]", "--")
        self.cpList = [m.start() for m in re.finditer(" ", q)]
        self.cpList.append(len(q))
        return True

    # confirm fetching
    def confirmFetch(self):
        # get message text
        messageText = self.getMessageText()
        # create message box
        msgBox = QtWidgets.QMessageBox(self.MainWindow)
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Confirm")
        msgBox.setText("Do you want to start fetching with the following pattern:")
        msgBox.setInformativeText(messageText)
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )
        clickedButton = msgBox.exec_()
        if clickedButton == QtWidgets.QMessageBox.Ok:
            self.startFetch()

    # get message text for confirm fetch
    def getMessageText(self):
        queryStart = self.searchItems[0]["q"]
        queryLast = self.searchItems[-1]["q"]
        cpCount = len(self.cpList)
        if cpCount < len(self.searchItems):
            queryNext = self.searchItems[cpCount]["q"]
            messageText = f"{queryStart}\n{queryNext}\n.\n.\n.\n{queryLast}"
            return messageText
        messageText = f"{queryStart}\n.\n.\n.\n{queryLast}"
        return messageText

    # start fetching
    def startFetch(self):
        self.proceed = True
        self.buttonStart.setEnabled(False)
        self.buttonStop.setEnabled(True)
        self.buttonReset.setEnabled(False)
        self.getAutocomplete()
        self.updateProgressBar(len(self.searchItems))
        self.buttonStart.setEnabled(True)
        self.buttonStop.setEnabled(False)
        self.buttonReset.setEnabled(True)
        self.buttonExport.setEnabled(True)
        if self.proceed:
            self.appendToConsole("Completed!", success=True)
            # self.buttonExport.click()

    # stop button on click callback
    def stopClicked(self):
        self.proceed = False
        self.appendToConsole("Stopped!", error=True)

    # reset button on click callback
    def resetClicked(self):
        self.lineEditQuery.setText("")
        self.LineEditRange.setText("")
        self.LineEditCP.setText("")
        self.textEditConsole.setText("")
        self.progressBar.setValue(0)
        self.clearErrorBeforeStart()
        self.proceed = True

    # export button on click callback
    def exportClicked(self):
        msgBox = QtWidgets.QMessageBox(self.MainWindow)
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setWindowTitle("Export As")
        msgBox.setText("How do you want to export?")
        msgBox.addButton(self.exportLabel["txt"], QtWidgets.QMessageBox.AcceptRole)
        msgBox.addButton(self.exportLabel["csv"], QtWidgets.QMessageBox.AcceptRole)
        msgBox.buttonClicked.connect(self.exportAs)
        msgBox.exec_()

    # export as on click callback function
    def exportAs(self, event):
        folder = os.path.join(os.path.expanduser("~"), "Desktop")
        buttonText = event.text()
        fullpath = self.getFullpath(folder, buttonText)
        if not fullpath:
            return
        output = self.processOutput(buttonText)
        with open(fullpath, "w", encoding="utf-8") as f:
            f.write(output)
        self.createMessageBoxExportConfirm(fullpath)

    # create a message box with file export confirmation
    def createMessageBoxExportConfirm(self, fullpath):
        msgBox = QtWidgets.QMessageBox(self.MainWindow)
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Saved")
        msgBox.setText(f"Output saved in file:\n{fullpath}")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Open)
        buttonClicked = msgBox.exec_()
        if buttonClicked == QtWidgets.QMessageBox.Open:
            os.startfile(fullpath)

    # get full path of the export file
    def getFullpath(self, folder, btnText):
        if btnText == self.exportLabel["txt"]:
            ext = ".txt"
        if btnText == self.exportLabel["csv"]:
            ext = ".csv"
        fname = QtWidgets.QFileDialog().getSaveFileName(
            self.MainWindow, "Save File", folder, ext
        )[0]
        if fname == "":
            return False
        fullpath = os.path.join(folder, fname + ext)
        return fullpath

    # process output text for export
    def processOutput(self, btnText):
        output = ""
        if btnText == self.exportLabel["txt"]:
            for item in self.searchItems:
                if "result" in item:
                    output = output + item["result"]
        if btnText == self.exportLabel["csv"]:
            for item in self.searchItems:
                if "result" in item:
                    q = item["q"]
                    cp = item["cp"]
                    result = item["result"]
                    for r in result.split("\n"):
                        line = f'"{q}","{cp}","{r}"\n'
                        output = output + line
            headerline = '"Query","Cursor Pos","Result"\n'
            output = headerline + output
        return output

    # log error in console
    def logError(self, msg, lineEdit):
        lineEdit.setStyleSheet("border: 1px solid red;")
        self.appendToConsole(msg, error=True)

    # create a generator for alphabet sequence
    def iter_all_strings(self, c):
        for size in itertools.count(c):
            for s in itertools.product(ascii_lowercase, repeat=size):
                yield "".join(s)

    # collect all alphabet sequence for query
    def getAlphabets(self, start, end, count):
        alphabets = []
        push = False
        for s in self.iter_all_strings(count):
            if s == start:
                push = True
            if push:
                alphabets.append(s)
                if s == end:
                    return alphabets

    # get all the search items [{query, cp}]
    def getSearchItems(self):
        self.searchItems = []
        if self.radioSingle.isChecked():
            start = self.rangeText[0]
            end = self.rangeText[2]
            count = 0
        if self.radioDouble.isChecked():
            start = self.rangeText[:2]
            end = self.rangeText[3:]
            count = 1
        alphabets = self.getAlphabets(start, end, count)
        for alphabet in alphabets:
            q = self.query.replace("[alphabet]", alphabet)
            for cp in self.cpList:
                self.searchItems.append({"q": q, "cp": cp})

    # get autocomplete data
    def getAutocomplete(self):
        for i, searchItem in enumerate(self.searchItems):
            if self.proceed:
                self.updateProgressBar(i + 1)
                q = searchItem["q"]
                cp = searchItem["cp"]
                self.appendToConsole(f"Fetching: {q} (cp={cp})")
                QtTest.QTest.qWait(1000)
                url = f"http://google.com/complete/search?client=gws-wiz-serp&cp={cp}&q={q}"
                response = requests.get(url, headers=self.headers)
                if response.ok:
                    responseText = response.content.decode()
                    fullText = self.processResults(q, responseText)
                    self.searchItems[i]["result"] = fullText
                    # for line in fullText.split("\n"):
                    #     self.appendToConsole(line)
                else:
                    self.appendToConsole(
                        f"Fetching failed, status={response.status_code}"
                    )

    def appendToConsole(self, txt, error=False, success=False):
        if error:
            msg = f'<span style="color: {self.colors["red"]};">{txt}</span>'
        elif success:
            msg = f'<span style="color: {self.colors["green"]};">{txt}</span>'
        else:
            msg = f'<span style="color: #000000;">{txt}</span>'
        contents = self.textEditConsole.toPlainText().strip()
        if contents == "":
            self.textEditConsole.append(msg)
        else:
            self.textEditConsole.append(f"\n{msg}")
        self.textEditConsole.verticalScrollBar().setValue(
            self.textEditConsole.verticalScrollBar().maximum()
        )

    # process the text response
    def processResults(self, query, txt):
        fullText = ""
        txt = re.sub(r"\\u003c.+?\\u003e", "", txt)
        start = txt.find("[[[")
        end = txt.find("]]]")
        if start != -1 and end != -1:
            results = txt[start:end].split("],[")
            for item in results:
                result = re.match('".+"', item)
                if result:
                    outputText = result.group(0).replace('"', "")
                    outputText = outputText.lower()
                    # outputTxt = outputTxt.replace('\u003cb\u003e', '')
                    # outputTxt = outputTxt.replace('\u003c\/b\u003e', '')
                    outputText = outputText.replace("\u0026#39;", "")
                    # outputTxt = re.sub(r"\\u003c.+?\\u003e", "", outputTxt)
                    outputText = outputText.encode().decode("unicode_escape")
                    fullText = f"{fullText}{outputText}\n"
        return fullText

    # update the progress bar
    def updateProgressBar(self, i):
        percentage = math.floor(i / len(self.searchItems) * 100)
        self.progressBar.setValue(percentage)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
