import csv
import os

def write_csv(receiver, sender, subject, body, datetime, email_class, attachment_type=None, filepath=None, password=None, mal="N/A", summary=None, class_of_doc=None):

    # if os.path.exists(f"{receiver}.csv"):
    #     os.remove(f"{receiver}.csv")
    # Create the CSV filename using the receiver's name
    csv_filename = f"/home/jfrans/Hackathon/Forensics/{receiver}.csv"
    
    # Check if the CSV file already exists
    if not os.path.exists(csv_filename):
        # Write header if the file doesn't exist
        header = ["Sender", "Subject", "Email Body", "Email Datetime", "Email Class", "Attachment Type", "Filepath", "Password", "Malware?", "Attachment Summary", "Class Of Attachment"]
        with open(csv_filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
    
    # Prepare the row data
    row_data = [sender, subject, body, datetime, email_class,  attachment_type, filepath, password, mal, summary, class_of_doc]
    
    # Write the row data to the CSV file
    with open(csv_filename, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(row_data)

def write_csv_local(csv_filename, file_type=None, password='N/A', mal="N/A", summary="WIP", class_of_doc="WIP"):

    # if os.path.exists(f"{receiver}.csv"):
    #     os.remove(f"{receiver}.csv")
    # Create the CSV filename using the receiver's name
    csv_filepath = f"/home/jfrans/Hackathon/Forensics/DevAnalysis.csv"


    # Check if the CSV file already exists
    if not os.path.exists(csv_filepath):
        # Write header if the file doesn't exist
        header = ["File Name","File Type", "Password", "Malware?", "Summary", "Class Of Attachment"]
        with open(csv_filepath, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)

    # Prepare the row data
    row_data = [csv_filename, file_type, password, mal, summary, class_of_doc]

    # Write the row data to the CSV file
    with open(csv_filepath, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(row_data)

# Example usage
# write_csv("receiver_name2", "sender@example.com", "Important Email", "Hello, this is an email.", "2023-08-22 12:00:00")
