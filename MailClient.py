from socket import *
import sys

class MailClient():
    """
    Simple Client for sending email
    """
    port = 25
    host = None
    helo_response = None
    socket = None

    def __init__(self, host):
        """
        :param host: hostname of mail server
        :return:
        """
        self.host = host
        if self.host:
            response = self.connect(host, self.port)
            code = response[0]
            # Server should reply with 220 if successful connection
            if code != 220:
                print "Server connection failed - Error: " + code
                sys.exit(0)
            print "Connected: " + response[1]

    def connect(self, host, port):
        """
        Establish socket connection
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((host, port))
        return self.get_response()

    def close(self):
        """
        Close the socket connection
        """
        self.socket.close()

    def quit(self):
        """
        Enters command QUIT into command line to close
        connection to mail server

        """
        self.socket.send("QUIT")

    def send_helo(self):
        """
        Send HELO hostname to server
        :return:
        """
        message = "HELO localhost"+"\r"+"\n"
        self.socket.send(message)
        response = self.get_response()
        if response[0] != 250:
            print "Error try again"
            print response[1]
            sys.exit(0)

    def send_mail_from(self, email_from):
        """
        Client sends MAIL FROM: <email_from>
        :return:
        """
        self.socket.send("MAIL FROM: %s\r\n" % email_from)
        response = self.get_response()
        if response[0] != 250:
            print "There was a problem with the from email"
            print response[1]
            sys.exit(0)

    def send_rcpt_to(self, email_to):
        """
        Client sends RCPT TO: <mail_to>
        :return:
        """
        self.socket.send("RCPT TO: %s\r\n" % email_to)
        response = self.get_response()
        if response[0] != 250:
            print "An error has occured. Try correcting the email address you are sending to"
            print response[1]
            sys.exit(0)

    def send_data(self):
        """
        Client sends DATA to server
        :return:
        """
        self.socket.send("DATA\r\n")
        response = self.get_response()
        if response[0] != 354:
            print "An error has occured try again"
            print response[1]
            sys.exit(0)

    def send_message(self, subject, message):
        """
        Send email message contents
        :return:
        """
        subject = "Subject: %s \n" % subject
        message += "\r\n.\r\n"
        self.socket.send(subject + message)
        response = self.get_response()
        if response[0] != 250:
            print "There was a problem sending the message try again"
            print response[1]
            sys.exit(0)
        print "Message being sent.. \n"
        print response

    def get_response(self):
        """
        Gets response from server
        Every response should begin with 3 digit error code
        ex: HELO gmail.com
            "250 mx.google.com at your server"
        :return: code and response message tuple
        """

        response = self.socket.recv(1024)
        code = response.split(" ")[0]
        message = response[4:]

        return int(code), message

    def print_error(self, code):
        """
        :param code: 3 digit code
        :return: void
        """
        if code == 500:
            print "There was a syntax error. Please try again"
        elif code == 501:
            print "There was a syntax error in parameters"
        elif code == 502:
            print "Error - A command was not implmented. Try again"
        elif code == 450:
            print "Mailbox unavailable or busy. Try again later"
        elif code == 550:
            "Mailbox not found - Try again"
        else:
            print "There was an error try again."

    def send_mail(self, email_to, email_from, email_subject, email_message):
        """

        :param email_to: email address being sent to
        :param email_from: email address being sent from
        :param email_message: email message contents
        :return:


        2. Send HELO
        3. Check that HELO response is 250
        4. Send MAIL FROM : email_from
        5. Check that response is 250
        6. Send RCPT TO: email_to
        7. Check for 250 response
        8. Send DATA
        9.
        """
        # send HELO to server
        self.send_helo()
        # send MAIL FROM:
        self.send_mail_from(email_from)
        self.send_rcpt_to(email_to)
        self.send_data()
        self.send_message(email_subject, email_message)


if __name__ == '__main__':
    host_name = "localhost"
    client = MailClient(host_name)
    mail_to = raw_input("Enter the email address you want to mail \n")
    mail_from = raw_input("Enter your email address \n")
    mail_subject = raw_input("Enter the subject for the message \n")
    print "Enter the email message \nEnter a period on a line by itself to end message"
    mail_message = ""
    while True:
        content = sys.stdin.readline()
        if content.strip() == ".":
            break
        mail_message += content
    client.send_mail(mail_to, mail_from, mail_subject, mail_message)
    client.quit()
