
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
import socket
import firebase

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
    
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")
        #
        self.nameIn = tk.Entry(self.groupCon, width=20)
        self.nameIn.insert(tk.END, 'Unnamed')
        self.nameIn.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")

        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
            command = clearButtonClick)
        self.clearButton.pack(side="left")

        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
            state=tk.DISABLED)
        self.msgText.pack(side="top")

        
        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', sendMessage)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupSend, text = 'send',
            command = sendButtonClick)
        self.sendButton.pack(side="left")
        
        
        # set the focus on the IP and Port text field
        self.nameIn.focus_set()

def clearButtonClick():
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.delete(1.0, tk.END)
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)


def sendButtonClick():
    # forward to the sendMessage method
    sendMessage(g_app)

# the connectHandler toggles the status between connected/disconnected


# a utility method to print to the message field        
def printToMessages(message):
    try:
        formatedMessage = message["name"]
        formatedMessage += ": "
        formatedMessage += message["text"]
    except:
        formatedMessage = message
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, formatedMessage + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

# if attempt to close the window, it is handled here
def on_closing():
    if tkmsgbox.askokcancel("Quit",
        "You are still connected. If you quit you will be"
        + " disconnected."):
        myQuit()
    else:
        myQuit()

# when quitting, do it the nice way    
def myQuit():
    message_stream.close()
    g_root.destroy()


# attempt to send the message (in the text field g_app.textIn) to the server
def sendMessage(master):
    msg = {
        "name": g_app.nameIn.get(),
        "text": g_app.textIn.get()
    }
    firebase.messages.push(msg)
    g_app.textIn.delete(0, 1023)



# launch the gui
g_root = tk.Tk()
g_app = Application(master=g_root)
message_stream = firebase.messages.listen(firebase.stream_handler_creator(printToMessages))


# if attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", on_closing)

# start the main loop
# (which handles the gui and will frequently call pollMessages)
g_app.mainloop()
