import base64
import datetime
import hashlib
import io
import random
import smtplib
from email.message import EmailMessage
from flask import jsonify
from src.utils.Constants import Constants
from src.utils.schema import SCHEMA


class Utils:

    GUEST = {
        'name': '$8Guest'
    }

    @classmethod
    def createList(cls, elements):
        response = []
        for element in elements:
            response.append(element.toJson())
        return response

    @classmethod
    def createFreeList(cls, elements):
        response = []
        for element in elements:
            response.append(element)
        return response

    @classmethod
    def createSuccessResponse(cls, success, param):
        return jsonify({
            "date": str(datetime.datetime.now()),
            "success": success,
            "param": param,
            "code": 200,
        })

    @classmethod
    def createWrongResponse(cls, success, error, code):
        return jsonify({
            "date": str(datetime.datetime.now()),
            "success": success,
            "error": error,
            "code": code,
        })

    @classmethod
    def getURL(cls, controllerName):
        return '/api/v1/' + controllerName

    @classmethod
    def hash(cls, password: str):
        return hashlib.md5(password.encode('UTF-8')).hexdigest()

    @classmethod
    def createLink(cls, length):
        letters = "ABCDEFGHILMNOPQRSTUVZYJKXabcdefghilmnopqrstuvzyjkx0123456789"
        link = ""
        for i in range(length):
            link += letters[random.randint(0, 59)]
        return link

    @classmethod
    def createCode(cls, length):
        letters = "ABCDEFGHILMNOPQRSTUVZYJKX0123456789"
        link = ""
        for i in range(length):
            link += letters[random.randint(0, 34)]
        return link

    @classmethod
    def sendPasswordForgottenEmail(cls, email, token):
        msg = EmailMessage()
        msg.set_content(Constants.PASSWORD_FORGOTTEN_EMAIL.replace("{token}", token))
        msg['Subject'] = 'Forget password'
        msg['From'] = Constants.EMAIL
        msg['To'] = email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(Constants.EMAIL, Constants.PASSWORD)
        server.send_message(msg)
        server.quit()

    @classmethod
    def decodeImage(cls, image, imageName):
        decodedImage = base64.b64decode(str(image))
        file = Image.open(io.BytesIO(decodedImage))
        file.save(imageName, 'png')

    @classmethod
    def encodeImage(cls, imageName):
        with open(imageName, "rb") as image:
            encodedImage = base64.b64encode(image.read())
        return str(encodedImage)

    @classmethod
    def isValid(cls, givenSchema, schemaName):
        for schema in SCHEMA:
            if schema['name'] == schemaName:
                for key in schema['schema']:
                    if key not in givenSchema or type(givenSchema[key]) != schema['schema'][key]:
                        return False
        return True

    @classmethod
    def createListOfPages(cls, array, pageLength):
        switchedElements = 0
        i = 0
        finalArray = []
        while len(array) != switchedElements:
            page = []
            for j in range(pageLength if len(array) - switchedElements > pageLength else len(array) - switchedElements):
                page.append(array[j + (i * pageLength)])
                switchedElements += 1
            i += 1
            finalArray.append(page)
        return finalArray

    @classmethod
    def fixNumber(cls, number):
        if number < 999:
            return str(number)
        if number > 999 and number < 10000:
            return str(number)[0]+"."+str(number)[1]+"k"
        if number > 9999 and number < 100000:
            return str(number)[0:2]+"."+str(number)[2]+"k"
        if number > 99999 and number < 1000000:
            return str(number)[0:3]+"."+str(number)[3]+"k"
        if number > 999999 and number < 10000000:
            return str(number)[0]+"."+str(number)[1:3]+"M"
        if number > 9999999 and number < 100000000:
            return str(number)[0:2]+"."+str(number)[2]+"M"
        if number > 99999999 and number < 1000000000:
            return str(number)[0:3]+"M"
        if number > 1000000000:
            return str(number)[0]+"MLD"

