import imaplib
import email
import os
import joblib
from pdftotext import check_file_extension, is_password_protected, decrypt_pdf
from readallfiles import read_file
from summary2 import summarize
from csv_write import write_csv
from PassCrack import GetHash, HashCat
import metric
import pandas as pd
import subprocess

#from credentials import useName, passWord
os.system("touch /home/jfrans/Hackathon/Forensics/susygrime@gmail.com_metric.csv")
os.system("touch /home/jfrans/Hackathon/Forensics/frankgrime123@gmail.com_metric.csv")

def load_and_predict(model_filename, new_data):
    loaded_model = joblib.load(model_filename)
    if(None in new_data):
        predictions = ""
    else:
        predictions = loaded_model.predict(new_data)
    return predictions

password_tmp = "uvxoyvwpiyytmpth"
imap_url ='imap.gmail.com'
my_mail = imaplib.IMAP4_SSL(imap_url)


def email_read(my_mail, receiver_id, password):
    my_mail = imaplib.IMAP4_SSL(imap_url)
    filePath = None
    my_mail.login(receiver_id, password)
    my_mail.select('Inbox') #check sent

    data = my_mail.search(None, 'All')
    mail_ids = data[1]  
    id_list = mail_ids[0].split(b' ')  
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    #remove csv if it already exists
    if os.path.exists(f"/home/jfrans/Hackathon/Forensics/{receiver_id}.csv"):
        os.remove(f"/home/jfrans/Hackathon/Forensics/{receiver_id}.csv")

    for i in range(latest_email_id,first_email_id, -1):
        password = None
        mal = None
        summary = None
        filePath = None
        fileExtension = None
        email_class = None
        class_of_doc = [""]
        data = my_mail.fetch(str(i), '(RFC822)' )
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):

                msg = email.message_from_bytes(arr[1])
                email_subject = msg['subject']
                index = (msg['from']).find('<')
                email_from = (msg['from'])[0:index]
                email_date =  msg['Date']
                email_body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            email_body = part.get_payload(decode=True).decode("utf-8")
                            break
                else:
                    email_body = msg.get_payload(decode=True).decode("utf-8")

                #print('From : ' + email_from)
                #print('Subject : ' + email_subject)
                #print('Date: ' + email_date + '\n')
                #print('Body: '+ email_body)
                email_class = load_and_predict('trained_model.joblib', [email_body+email_subject])
                #print(email_class)

                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    fileName = part.get_filename()

                    acceptable_filetypes = ["PDF", "Word", "Text"]

                    if check_file_extension(fileName) not in acceptable_filetypes:
                        print("UNACCEPTABLE " + fileName)
                        continue
                    
                    if bool(fileName):
                        filePath = "/home/jfrans/Hackathon/Forensics/" + fileName
                        if not os.path.isfile(filePath) :
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                        if is_password_protected(filePath):
                            filetype = filePath[filePath.rfind('.')+1:]
                            HashCat('y','y','y','y',1,16,GetHash(filePath,filetype))
                            with open("/home/jfrans/Desktop/Password.txt","r") as passfile:
                                tmp = passfile.readline()
                                password = tmp[tmp.rfind(":")+1:].strip()
                            #print(filePath)
                            decrypt_pdf(filePath, password)

                            base_name, extension = os.path.splitext(fileName)
                            #file_name = os.path.join(filePath, base_name + '_decrypted'+ extension)
                            file_name = "/home/jfrans/Hackathon/Forensics/" + base_name + "_decrypted" + extension
                            #print(file_name)
                            pdf_content = read_file(file_name)
                            summary = summarize(file_name)
                            class_of_doc = load_and_predict('/home/jfrans/Hackathon/Forensics/trained_model_doc.joblib', [pdf_content]).tolist()
                            #input(type(class_of_doc))

                        #add other formats here with conditions
                        else:
                            #print(filePath)
                            pdf_content = read_file(filePath)
                            summary = summarize(filePath)
                            class_of_doc = load_and_predict('/home/jfrans/Hackathon/Forensics/trained_model_doc.joblib', [pdf_content]).tolist()
                            #input(type(class_of_doc))
                        #if summary:
                            #print("SUMMARY: " + summary)
                        #if class_of_doc:
                            #print("Class of DOc: ", class_of_doc[0])

                        fileExtension = check_file_extension(filePath)
        if filePath == None:
            mal = None
        elif subprocess.run(["malwaredetect",filePath],stdout=subprocess.PIPE,text=True).stdout == "":
            mal = "Clean"
        else:
            mal = "Potential Malware"
        write_csv(receiver_id, email_from, email_subject, email_body, email_date, email_class[0], fileExtension, filePath, password, mal, summary, class_of_doc[0])


                            
                            

        # my_mail.expunge()
    my_mail.close()
    my_mail.logout()
    sender_rep = metric.reputation_count(f"/home/jfrans/Hackathon/Forensics/{receiver_id}.csv")
    add_metric(f"/home/jfrans/Hackathon/Forensics/{receiver_id}.csv", f"/home/jfrans/Hackathon/Forensics/{receiver_id}_metric.csv", sender_rep)
    return f"/home/jfrans/Hackathon/Forensics/{receiver_id}_metric.csv"
#email_read(my_mail)

def add_metric(csv_file, reciever_file, sender_rep):
    try:
        df = pd.read_csv(csv_file)

        df['Ranking'] = (
            df.apply(lambda row: metric.email_length(str(row['Body'])) * 1 +
                                 metric.sentiment(str(row['Body'])) * 4 +
                                 metric.urgency(str(row['Body'])) * 3 +
                                 metric.attachment_present(str(row['Attachment Type'])) * 2 +
                                 sender_rep * 5 +
                                 metric.email_class(str(row['Class'])) * 6,
                     axis=1)
        )

        df.to_csv(reciever_file, index=False)
        print("Done processing and saving.")
    except Exception as e:
        print(e)
        print("An error occurred.")
