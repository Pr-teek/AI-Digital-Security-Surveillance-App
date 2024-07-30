import SendEmail

msg = SendEmail.generate("jfrans@127.0.0.2", "jfrancis4142@gmail.com", "Potential CN Project", "Hello,\n This is ACER PREDATOR HELIOS 300 PH315-53.\nBye.\nRegards,\nACER PREDATOR HELIOS 300 PH315-53","/home/jfrans/Hackathon/Forensics/DevAnalysis.csv")

SendEmail.send(msg)
