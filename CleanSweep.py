#!/usr/bin/python

from tkinter import *
from tkinter import filedialog 
import os
import re
from pdftotext import decrypt_pdf
from readallfiles import read_file
from summary2 import summarize
from csv_write import write_csv_local
from ScanDevice import *
root = Tk()
root.geometry("500x200")
root.title("Flash/Drive")
from emails import email_read
import imaplib
from PassCrack import *
from file_share import *
from emails import load_and_predict

imap_url ='imap.gmail.com'
my_mail = imaplib.IMAP4_SSL(imap_url)
listenc = []
os.system("touch /tmp/bad.txt")
#pw cracker

#takes only num
def only_numbers(char):
    return char.isdigit()

#checks if min/max >1
def check(v1,v2,v3,v4,gpu,minv,maxv,path):
    with open("/tmp/bad.txt","r") as bad:
        path = bad.readline().strip()
    filetype = path[path.rfind('.')+1:]
    jhash = GetHash(path,filetype)
    if gpu == 'y':
        HashCat(v1,v2,v3,v4,minv,maxv,jhash)
    else:
        JohnTR(v1,v2,v3,v4,minv,maxv,filetype,jhash)
    with open("/home/jfrans/Desktop/Password.txt","r") as passfile:
        tmp = passfile.readline()
        password = tmp[tmp.rfind(":")+1:].strip()
        filename = tmp[tmp.rfind("/"):tmp.rfind(":")+1].strip()
        execute(password)
    mini = int(box_min.get())
    maxi = int(box_max.get())
    box_min.delete(0,END)
    box_max.delete(0,END)
    answer_max.config(text="")
    answer_min.config(text="")
    if mini >= 1 and maxi >= 1:
        return
    else:
        if mini<1:
            box_min.delete(0,END)
            answer_min.config(text="Value should be greater than 1")

        if maxi<1:
            box_max.delete(0,END)
            answer_max.config(text="Value should be greater than 1")

def execute(x):
    Execute = Toplevel()
    Execute.geometry("200x100")

    result = Label(Execute,text="Password :")
    result.grid(row=2,column=0,padx=30,pady=35)
    output = Text(Execute,height=1,width=45,border=0,bg="#f0f0f0")
    output.grid(row=2,column=1,columnspan=3)
    output.insert(END,x)
    output.config(state="disabled")

#main window
def pwWindow():
    pas = Toplevel()
    pas.title("Flash/Drive")
    pas.geometry("800x450")

    validation = pas.register(only_numbers)
    
    #project title
    Proj_Title = Label(pas, text="Flash/Drive",fg="#040c4d")
    Proj_Title.config(font=("Courier", 32, "bold"))
    Proj_Title.grid(row=0,column=0,columnspan=3,padx=8,pady=1,sticky='w')

    #Title
    Title = Label(pas, text="Password Cracking")
    Title.config(font=("Helvetica", 11, "italic"))
    Title.grid(row=1,column=0,padx=10,sticky='w', columnspan=2)
    #browse file
    def openfile():
        filepath = filedialog.askopenfilename(initialdir="/home/jfrans/",
                                            title="open file okay?",
                                            filetypes=(("All Files","*.*"),
                                            ("Pdf Files","*.pdf"),
                                            ("Text Files","*.txt")))
        file = open(filepath,'r')

        output = Text(pas,height=1,width=45,border=0,bg="#f0f0f0")
        output.grid(row=3,column=2,columnspan=3)
        output.insert(END,os.path.basename(filepath).split('/')[-1])
        output.config(state="disabled")
        file.close()
        os.system("echo "+filepath+" > /tmp/bad.txt")


    l1 = Label(pas, text="Choose processing unit: ")
    l1.grid(row=2,column=0,sticky = 'w',padx= 20,pady=15)
    PUvalue = StringVar(value='n')
    r1 = Radiobutton(pas,text="CPU",padx=14,variable=PUvalue,value='n')
    r1.grid(row=2,column=1,sticky='w')
    r2 = Radiobutton(pas,text="GPU",padx=14,variable=PUvalue,value='y')
    r2.grid(row=2,column=2,sticky='w')

    file = Label(pas, text="Select File:")
    file.grid(row=3,column=0,pady=5,sticky = 'w', padx= 20)
    btn1 = Button(pas, text="Browse files",command=openfile)
    btn1.grid(row=3,column=1,pady=15,sticky = 'w')
    
    #choose characters
    char_label = Label(pas, text = "Choose Type of Characters present: ")
    char_label.grid(row=4,column=0,sticky = 'w', padx= 20, pady=18)

    var1 = StringVar(value=0)
    var2 = StringVar(value=0)
    var3 = StringVar(value=0)
    var4 = StringVar(value=0)

    c_UC = Checkbutton(pas, text="Upper Case", variable = var1, onvalue="y", offvalue="n")
    c_UC.deselect()
    c_UC.grid(row=4,column=1,sticky = 'w')

    c_LC = Checkbutton(pas, text="Lower Case", variable = var2, onvalue="y", offvalue="n")
    c_LC.deselect()
    c_LC.grid(row=4,column=2,sticky = 'w')

    c_num = Checkbutton(pas, text="Number", variable = var3, onvalue="y", offvalue="n")
    c_num.deselect()
    c_num.grid(row=4,column=3,sticky = 'w',padx=45)

    c_Sym = Checkbutton(pas, text="Symbol", variable = var4, onvalue="y", offvalue="n")
    c_Sym.deselect()
    c_Sym.grid(row=4,column=4,sticky = 'w')

    # min max password
    global box_max, box_min, answer_max, answer_min

    min_label = Label(pas, text="Minimum length of password:")
    min_label.grid(row=5, column=0,sticky = 'w', padx= 20, pady=5)

    box_min = Entry(pas,validate="key",validatecommand=(validation,"%S"))
    box_min.grid(row=5, column=1, padx=5,sticky = 'w')

    answer_min = Label(pas, text='')
    answer_min.grid(row=6, column=1, padx=10)
    
    max_label = Label(pas, text="Maximum length of password:")
    max_label.grid(row=7, column=0, sticky = 'w', padx= 20)

    box_max = Entry(pas,validate="key",validatecommand=(validation,"%S"))
    box_max.grid(row=7, column=1, padx=5,pady=20,sticky = 'w')

    answer_max = Label(pas, text='')
    answer_max.grid(row=8, column=1, padx=10)
    with open("/tmp/bad.txt","r") as bad:
        fpath = bad.readline().strip()
    pw_sub = Button(pas, text="Execute", command=lambda: check(var1.get(),var2.get(),var3.get(),var4.get(),PUvalue.get(),box_min.get(),box_max.get(),fpath), padx=10, pady=5,activebackground='#cadee8')
    pw_sub.grid(row=9, column=0, padx=25)

#Scan Drive
def scan():
    def openFile():
        os.system("libreoffice --calc /home/jfrans/Hackathon/Forensics/DevAnalysis.csv")

    def analyze(scan_drive_data):
        analyze_data = Toplevel()
        analyze_data.geometry("300x200")
        scan_drive_data.destroy()

        Title_label = Label(analyze_data, text="Analysis Completed!")
        Title_label.config(font=("Helvetica", 12, "italic"))
        Title_label.grid(row=0, column=0, padx=15, pady=(15,0))

        path_label = Label(analyze_data, text="CSV File Created")
        path_label.config(font=("Helvetica", 10))
        path_label.grid(row=1, column=0, padx=(35,0), pady=(15,0))

        close_btn = Button(analyze_data,text="Open file",command = lambda: [openFile(), analyze_data.destroy()], activebackground='#cadee8')
        close_btn.grid(row=2,column=0,padx=(55,0), pady=25)

        open_btn = Button(analyze_data,text="Close",command = lambda: analyze_data.destroy(), activebackground='#cadee8')
        open_btn.grid(row=2,column=1, padx=(0,55),pady=25)

    #list
    def Proceed(sdev,ch):
        scan_drive_data = Toplevel()
        scan_drive_data.geometry("525x320")
        scan_drive_data.title("Flash/Drive")

        Title_label = Label(scan_drive_data, text="Files Found:")
        Title_label.config(font=("Helvetica", 12, "italic"))
        Title_label.grid(row=0, column=0, padx=15, pady=(15,5))

        analyze_btn = Button(scan_drive_data,text="Analyze",command= lambda: [Crack(),analyze(scan_drive_data)], activebackground='#cadee8')
        analyze_btn.grid(row=2,column=0,pady=(15,0),padx=(0,20))

        #list = {'temporary','hello','hiiiiii','list','project','number','3500','i','phone'}
        #pth = {"Acer":"nvme0n1p3","Data":"sda1","Target":"sdb1"}
        list1 = Scan(sdev)
        file_list = Text(scan_drive_data,height=12,width=75,border=0,bg="#f0f0f0")
        file_list.grid(row=1,column=0)
        list2 = FindEncryptedFiles(list1)
        if(ch==1):
            list1 = list2
        global listenc
        listenc = list2
        for i in list1:
            file_list.insert(END, "\t   "+i+"\n")
        file_list.config(state="disabled")

        #scrollbar
        sb = Scrollbar(
            scan_drive_data,
            orient=VERTICAL,
            width=20
        )
        sb.grid(row=1, column=1, sticky=NS,padx=35)
        file_list.config(yscrollcommand=sb.set)
        sb.config(command=file_list.yview)
        
    def Crack():
        csv_filepath = f"/home/jfrans/Hackathon/Forensics/DevAnalysis.csv"
        # Check if the CSV file already exists
        if os.path.exists(csv_filepath):
            os.system("rm /home/jfrans/Hackathon/Forensics/DevAnalysis.csv")

        for i in listenc:
            mal = None
            password = ""
            path = i.strip()
            filetype = path[path.rfind('.')+1:]
            jhash = GetHash(path,filetype)
            filename = path[path.rfind('/')+1:]
            HashCat('y','y','y','y',"1","32",jhash)
            with open("/home/jfrans/Desktop/Password.txt","r") as passfile:
                tmp = passfile.readline()
                password = tmp[tmp.rfind(":")+1:].strip()
            if password == "":
                HashCat('n','n','y','n',"1","10",jhash)
            with open("/home/jfrans/Desktop/Password.txt","r") as passfile:
                tmp = passfile.readline()
                password = tmp[tmp.rfind(":")+1:].strip()
            if password == "":
                password = "Failed"

            if filetype not in "pdf":
                write_csv_local(filename, filetype, password)
                continue
            decrypt_pdf(path, password)

            base_name, extension = os.path.splitext(path)
            #file_name = os.path.join(filePath, base_name + '_decrypted'+ extension)
            file_name =  base_name + "_decrypted" + extension
            #print(file_name)
            pdf_content = read_file(file_name)
            summary = summarize(file_name)
            class_of_doc = load_and_predict('/home/jfrans/Hackathon/Forensics/trained_model_doc.joblib', [pdf_content])
            if(not type(class_of_doc) == str):
                class_of_doc = class_of_doc.tolist()[0]
            syscmd = subprocess.run(["malwaredetect",path],stdout=subprocess.PIPE,text=True)
            if syscmd.stdout == "":
                mal = "Clean"
            else:
                mal = "Potential Malware"
            write_csv_local(filename, filetype, password, mal, summary, class_of_doc)


    def scan_drive_selected(option):
        if option == "--Select--":
            scan_btn.config(state="disabled")
            scan_btn1.config(state="disabled")
        else:
            scan_btn.config(state="normal")
            scan_btn1.config(state="normal")



    #main window
    scan_drive = Toplevel()    
    scan_drive.geometry("450x250")
    scan_drive.title("Flash/Drive")

    #project title
    Proj_Title = Label(scan_drive, text="Flash/Drive",fg="#040c4d")
    Proj_Title.config(font=("Courier", 32, "bold"))
    Proj_Title.grid(row=0,column=0,columnspan=3,padx=8,pady=1,sticky='w')

    #Title
    Title = Label(scan_drive, text="Scanning the Drive")
    Title.config(font=("Helvetica", 11, "italic"))
    Title.grid(row=1,column=0,padx=10,sticky='w', columnspan=2)

    menu= StringVar()
    menu.set("--Select--")

    select = Label(scan_drive, text="Select Drive:")
    select.grid(row=2, column=0, padx=20, pady=25)

    drop= OptionMenu(scan_drive, menu,*FindDevices(),command=scan_drive_selected)
    drop.grid(row=2,column=1)

    scan_btn = Button(scan_drive,text="Scan Everything",command=lambda: [Proceed(menu.get(),0),scan_drive.destroy()],activebackground='#cadee8')
    scan_btn1 = Button(scan_drive,text="Scan Encrypted",command=lambda: [Proceed(menu.get(),1),scan_drive.destroy()],activebackground='#cadee8')
    scan_btn.grid(row=3,column=2,padx=(10,10), pady=35)
    scan_btn1.grid(row=3,column=1,padx=(70,0), pady=35)

    scan_btn.config(state="disabled")
    scan_btn1.config(state="disabled")

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' #for scrape email        

#Scrape Mail
def mail():
    send_csv_mail_flag = True
    def mailEntry():
        #input("Got There")
        if value.get()=="sm":
            box_mail.config(state="normal")
            send_csv_mail_flag = True
        else:
            box_mail.config(state="disabled")
            #send_csv_mail_flag = False


    def getDetails(recep):
        email_1_value = box_1.get()
        password_1_value = box_2.get()
        filepath = email_read(my_mail, email_1_value, password_1_value)
        if(send_csv_mail_flag):
            #SEND EMAIL
            mail_file(filepath,recep)
        else:
            mail_file(filepath)


    scrape = Toplevel()       
    scrape.title("Flash/Drive")
    scrape.geometry("400x400")

    #project title
    Proj_Title = Label(scrape, text="Flash/Drive",fg="#040c4d")
    Proj_Title.config(font=("Courier", 32, "bold"))
    Proj_Title.grid(row=0,column=0,columnspan=3,padx=8,pady=1,sticky='w')

    #Title
    Title = Label(scrape, text="Email Scraping")
    Title.config(font=("Helvetica", 11, "italic"))
    Title.grid(row=1,column=0,padx=10,sticky='w', columnspan=2)

    email_1 = Label(scrape, text="Enter Email:")
    email_1.grid(row=2,column=0,padx=10, pady=20,sticky = 'w')

    box_1 = Entry(scrape)
    box_1.grid(row=2,column=1)


    scr_pw = Label(scrape, text="Enter Password:")
    scr_pw.grid(row=3,column=0,padx=10, pady=10,sticky = 'w')

    box_2 = Entry(scrape)
    box_2.grid(row=3,column=1)


    value = StringVar(value=0)
    sendMail = Checkbutton(scrape,text="Send file as a mail",variable=value,onvalue="sm",offvalue="no_sm",command=mailEntry)
    sendMail.deselect()
    sendMail.grid(row=4,column=0,sticky = 'w',padx=10,pady=20)


    mailLabel = Label(scrape, text="Enter reciever's e-mail")
    mailLabel.grid(row=5,column=0,padx=10,sticky = 'w')

    box_mail = Entry(scrape,state="disabled")
    box_mail.grid(row=5,column=1)

    scrape_sub = Button(scrape,text="Scrape",command=lambda: getDetails(box_mail.get()), activebackground='#cadee8')
    scrape_sub.grid(row=6,column=1,padx=15, pady=25)

def Dummy():
    pass

#project title
Proj_Title = Label(root, text="Flash/Drive",fg="#040c4d")
Proj_Title.config(font=("Courier", 32, "bold"))
Proj_Title.grid(row=0,column=0,columnspan=3,padx=10,pady=15,sticky = 'w')

#Title
Title = Label(root, text="Select desired option:")
Title.config(font=("Helvetica", 11, "italic"))
Title.grid(row=1,column=0,padx=10, columnspan=2,sticky = 'w')

#password cracking button
c_pw = Button(text="Crack Password",command=pwWindow, activebackground='#cadee8')
c_pw.grid(row=2,column=1,padx=5, pady=25)

#Scan drive button
s_drive = Button(root,text="Scan Device",command=scan, activebackground='#cadee8')
s_drive.grid(row=2,column=2,padx=15, pady=25)

#Scrape mail
scrape = Button(root,text="Scrape Email",command=mail, activebackground='#cadee8')
scrape.grid(row=2,column=3,padx=15, pady=25)

root.mainloop()
