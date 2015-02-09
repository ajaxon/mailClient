from socket import *


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
                # throw connect error
                pass
            print response

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
            raise Exception

    def send_mail_from(self, email_from):
        """
        Client sends MAIL FROM: <email_from>
        :return:
        """
        self.socket.send("MAIL FROM: %s\r\n" % email_from)
        response = self.get_response()
        if response[0] != 250:
            pass
        print response

    def send_rcpt_to(self, email_to):
        """
        Client sends RCPT TO: <mail_to>
        :return:
        """
        self.socket.send("RCPT TO: %s\r\n" % email_to)
        response = self.get_response()
        if response[0] != 250:
            pass
        print response

    def send_data(self):
        """
        Client sends DATA to server
        :return:
        """
        self.socket.send("DATA\r\n")
        response = self.get_response()
        if response[0] != 354:
            pass
        print response

    def send_message(self, message):
        """
        Send email message contents
        :return:
        """
        message += "\r\n.\r\n"
        self.socket.send(message)
        response = self.get_response()
        if response[0] != 250:
            pass
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

    def send_mail(self, email_to, email_from, email_message):
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

        self.send_mail_from(email_from)
        self.send_rcpt_to(email_to)
        self.send_data()
        self.send_message(email_message)


if __name__ == '__main__':
    host_name = raw_input("Enter the mailserver name")
    client = MailClient(host_name)
    mail_to = raw_input("Enter the email address you want to mail")
    mail_from = raw_input("Enter your email address")
    mail_message = raw_input("Enter the message you wish to send ")
    client.send_mail(mail_to, mail_from, mail_message)