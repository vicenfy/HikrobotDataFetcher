#####################
#### This script parses the CSV data as JSON objects and sends them HTTP calls
#### Copyright: SoGoo International GmbH
#####################

import csv
import requests
import json

baseUrl = 'http://localhost:8080/api/v1'

def createInstanceInDB(url, payload):
    return requests.request("POST", url, data=payload)

def readCsvAndWrite(filePath, productEndpoint):
    with open(filePath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='#')
        titleList = []
        for idx, row in enumerate(csv_reader):
            if idx == 0:
                titleList = row
            else:
                rowDataDict = {}
                for i in range(len(titleList)):
                    rowDataDict[titleList[i]] = row[i]
                jsonString = json.dumps(rowDataDict)
                createInstanceInDB(baseUrl + '/' + productEndpoint, jsonString)

readCsvAndWrite('c:\\hikdata\\Hik\\Area_Scan_Camera_with_Details\\' + 'caTable.csv', 'ascameras')