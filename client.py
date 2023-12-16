from tkinter import *
from tkinter import ttk
import socket
import threading

root=Tk()
cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#style - UI
root.title("Flight Client")
style=ttk.Style()
root.configure(background='#e1d8b2')
style.theme_use('classic')
style.configure('TLabel',background='#e1d8b2')
style.configure('TButton',background='#e1d8b2')
style.configure('TRadioButton',background='#e1d8b2')
font1=('Arial',16)

#Username - UI
username_label=ttk.Label(root, text="Username: ")
username_label.grid(row=0, column=0)
username_entry=ttk.Entry(root)
username_entry.grid(row=0, column=1, columnspan=2)

#Flight AICO
icao_label=ttk.Label(root, text="ICAO code: ")
icao_label.grid(row=1, column=0)
icao_entry=ttk.Entry(root)
icao_entry.grid(row=1, column=1, columnspan=2)

#Choose Option - UI
askToChoose=ttk.Label(root, text="Please choose an Option To request")
askToChoose.grid(row=2,column=0)
OptionChose=IntVar()
rb1=ttk.Radiobutton(root,text='A. Arrived Flights',variable=OptionChose,value=1)
rb1.grid(row=2, column=1)
rb2=ttk.Radiobutton(root,text='B. Delayed Flights',variable=OptionChose,value=2)
rb2.grid(row=2, column=2)
rb3=ttk.Radiobutton(root,text='C. Flights from Specific City',variable=OptionChose,value=3)
rb3.grid(row=3, column=1)
rb4=ttk.Radiobutton(root,text='D. Details of a Particular Flight',variable=OptionChose,value=4)
rb4.grid(row=3, column=2)

#Requested Data - UI
ttk.Label(root,text="The Requested data:").grid(row=4, column=0)
txtRequestedData=Text(root, width=30, height=15, font=font1)
txtRequestedData.grid(row=4, column=1, columnspan=2)

#Request/Quit - UI
buRequest=ttk.Button(root,text='Request')
buRequest.grid(row=5, column=3)
buQuit=ttk.Button(root,text='Quit')
buQuit.grid(row=5, column=2)



def ReceiveInformationAndSendIt():
    username = username_entry.get()
    username_entry.delete(0, END)
    icao = icao_entry.get()
    icao_entry.delete(0, END)
    def network_task():
        cs.connect(("127.0.0.1", 49999))
        data, addr = cs.recvfrom(4096)
        print(f"Server >> {data.decode()}")
        cs.send(icao.encode())
        data, addr = cs.recvfrom(4096)
        cs.send(str(OptionChose.get()).encode('ascii'))
        
    network_thread = threading.Thread(target=network_task)
    network_thread.start()
def goodBye():
    #TODO: Quit
    print("Bye!")
    
buRequest.config(command=ReceiveInformationAndSendIt)
buQuit.config(command=goodBye)
root.mainloop()