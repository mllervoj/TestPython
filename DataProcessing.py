import numpy as np
import pandas as pd

import logging

from configparser import ConfigParser

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class DataProcessing:
    def __init__(self, file):
        #Načtení konfiguračního souboru
        self.configur = ConfigParser()
        self.configur.read('config.ini')

        #Načtení dat
        self.data = pd.read_excel(file, decimal=',')
        fileFormat = '.' + file.split('.')[-1]

        #Uložení CSV
        self.csvPath = file.replace(fileFormat, '.csv')
        self.csvName = self.csvPath.split('/')[-1]
        self.data.to_csv(self.csvPath, encoding='utf-8', decimal=',')

        #Nastavení logování
        logPath = file.replace(fileFormat, '_statistika.log')
        logging.basicConfig(filename=logPath,
                            format='%(asctime)s: %(levelname)s: %(message)s',
                            level=logging.INFO)

        logging.info("Vytvoření instance třídy DataProcessing.")

    #Počet řádků
    def rowCount(self):
        rowCount = self.data.shape[0]
        logging.info("Počet záznamů: " + str(rowCount))
        return rowCount

    #Počet sloupců
    def columnCount(self):
        columnCount = self.data.shape[1]
        logging.info("Počet sloupců: " + str(columnCount))
        return columnCount

    #Počet unikátních hodnot ve sloupci
    def uniqueColumnCount(self, column):
        columnData = self.data[column]
        uniqueData = len(columnData.dropna().unique())
        logging.info("Počet unikátních dat ve sloupci " + column + ": " + str(uniqueData))
        return uniqueData

    #Počet prázdných hodnot ve sloupci
    def emptyColumnCount(self, column):
        columnData = self.data[column]
        emptyData = columnData.shape[0] - columnData.dropna().shape[0]
        logging.info("Počet prázdných záznamů ve sloupci " + column + ": " + str(emptyData))
        return emptyData

    #Průměr sloupcé, který je číselný
    def meanColumn(self, column):
        columnData = self.data[column]
        number = True
        for i in columnData:
            if isinstance(i, (int, float)):
                pass
            else:
                number = False
        if number:
            meanData = np.mean(columnData)
        else:
            meanData = 'Sloupec neobsahuje čísla'
        logging.info("Průměrná hodnota ve sloupci " + column + ": " + str(meanData))
        return meanData

    # Průměr sloupcé, který je číselný
    def minColumn(self, column):
        columnData = self.data[column]
        number = True
        for i in columnData:
            if isinstance(i, (int, float)):
                pass
            else:
                number = False
        if number:
            minData = np.min(columnData)
        else:
            minData = 'Sloupec neobsahuje čísla'
        logging.info("Minimální hodnota ve sloupci " + column + ": " + str(minData))
        return minData

    # Průměr sloupcé, který je číselný
    def maxColumn(self, column):
        columnData = self.data[column]
        number = True
        for i in columnData:
            if isinstance(i, (int, float)):
                pass
            else:
                number = False
        if number:
            maxData = np.max(columnData)
        else:
            maxData = 'Sloupec neobsahuje čísla'
        logging.info("Maximální hodnota ve sloupci " + column + ": " + str(maxData))
        return maxData

    # Odeslání mailu
    def sendMail(self, senderAddress, recipientAddress, senderPassword):
        # Nastavení parametrů mailu
        subject = "Test_CSV"
        body = ("Dobrý den, " + "\n" +
                "zasílám csv soubor s daty." + "\n" + "\n" +
                "S pozdravem" + "\n" +
                "Vojtěch Müller")
        sender_email = senderAddress
        recipient_email = recipientAddress
        sender_password = senderPassword
        path_to_file = self.csvPath

        # Nastavení SMTP
        SMTP = recipientAddress.split("@")[-1]
        smtp_server = self.configur.get(SMTP, 'root')
        smtp_port = self.configur.getint(SMTP, 'port')

        # Vytvoření mailu
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_email
        body_part = MIMEText(body)
        message.attach(body_part)

        # Připojení přílohy
        with open(path_to_file, 'rb') as file:
            message.attach(MIMEApplication(file.read(), Name=self.csvName))

        # Odeslání mailu
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        logging.info("Soubor CSV zaslán mailem.")


