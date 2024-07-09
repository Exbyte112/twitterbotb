from tempmail import EMail

def get_email():
    email = EMail()
    #print(email)
    return email.address

def get_email_message(email_adress, count=1):
    print(f"Getting email message from {email_adress}")
    email = EMail(address=email_adress)
    inboxes = email.get_inbox()
    try:
        if len(inboxes) == 0 and count < 5:
            print("No message yet\nRetrying...")
            return get_email_message(email_adress, count+1)
        elif len(inboxes) == 0 and count >= 5:
            print("No message yet\nExiting...")
            return None
        for inbox in inboxes:
            # get the first word of the subject
            first_word = inbox.message.subject.split(" ")[0]
            print(f"Verification code: {first_word}")
            return first_word
            break
    except:
        import time
        time.sleep(5)
        print("No message yet\nRetrying...")
        if count >= 5:
            print("No message yet\nExiting...")
            return None
        else:
            return get_email_message(email_adress, count+1)
    return None

def get_full_email_message(email_address):
    email = EMail(address=email_address)
    inboxes = email.get_inbox()
    try:
        if len(inboxes) == 0:
            print("No message yet\nRetrying...")
            return get_full_email_message(email_address)
        for inbox in inboxes:
            print(f"Message: {inbox.message.text_body}")
            return inbox.message.body
            break
    except:
        import time
        time.sleep(5)
        print("No message yet\nRetrying...")
        return get_full_email_message(email_address)
    return None
#print(get_email())
#get_email_message("mzpbacymek@vjuum.com")

get_full_email_message("nhlawlpkvh@dpptd.com")
