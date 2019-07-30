__author__= 'Furkan Goksel'
'''
MIT License

Copyright (c) 2019 Furkan Göksel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from burp import IBurpExtender #By Default is com(ing from API
from burp import IContextMenuFactory
from burp import IHttpRequestResponse
from java.util import ArrayList
from javax.swing import JMenuItem
from javax.swing import JFileChooser
from javax.swing import JPanel
from javax.swing.filechooser import FileSystemView
from java.io import PrintWriter

class BurpExtender(IBurpExtender,IContextMenuFactory): #Starter Class for Burp
#inherits from IBurpExtender,IProxyListener,IRepeaterListener
    def registerExtenderCallbacks(self, callbacks): #Register The Tabs
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._stdout = PrintWriter(callbacks.getStdout(),True)
        callbacks.setExtensionName("File Uploader")
        callbacks.issueAlert("File Uploader is started")
        callbacks.registerContextMenuFactory(self)

    def createMenuItems(self,invocation):
        self._invocation = invocation
        self.context = invocation.getInvocationContext()
        self._position = invocation.getSelectionBounds()
        tool = invocation.getToolFlag()
        if(tool == self._callbacks.TOOL_REPEATER or tool == self._callbacks.TOOL_PROXY):
            if(self.context in [invocation.CONTEXT_MESSAGE_EDITOR_REQUEST]):
                self._message = invocation.getSelectedMessages()
                #messageDeneme = self._message.getRequest()
                self._request = self._helpers.bytesToString(self._message[0].getRequest())
                menuList = ArrayList()
                menuItem = JMenuItem("Upload File Content",actionPerformed=self.readFromTheFile)
                menuList.add(menuItem)
                return menuList


    def readFromTheFile(self,event):
        choseFile = JFileChooser(FileSystemView.getFileSystemView().getHomeDirectory());
        choseFile.setDialogTitle('Select The File Which Will Be Pasted')
        choseFile.setFileSelectionMode(JFileChooser.FILES_ONLY)
        returnValue = choseFile.showOpenDialog(None);
        if(returnValue == JFileChooser.APPROVE_OPTION):
            selectedFile = choseFile.getSelectedFile()
            file=open(selectedFile.getAbsolutePath(),"r")
            editedRequest = self._request[:self._position[0]]+str(file.read())+self._request[self._position[1]:]
            self._message[0].setRequest(self._helpers.bytesToString(editedRequest))
