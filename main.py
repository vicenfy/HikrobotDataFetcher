#####################
#### This script sends HTTP calls to fetch the data from websites and parses the data as JSON objects
#### Copyright: SoGoo International GmbH
#####################

import requests

baseUrl = 'https://www.hikrobotics.com'
summaryListUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductContent?'
detailUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductConfig?'


def getSummaryData():
    paramsSummary = {'firstModuleId': 78, 'page': 1, 'secondaryModuleId': 42, 'size': 50, 'screening': None}
    resp = requests.get(summaryListUrl, paramsSummary)
    data = resp.json()
    visionProductConfig = data['data']['VisionProductConfig']
    visionProductContent = data['data']['VisionProductContent']['records']
    titles = ['Product Model', 'Sensor', 'Resolution', 'Max. Frame Rate', 'Mono/Color']
    # make sure that the title list and the data have the same dimension
    print('Trying to export CSV file for the summary')
    exportObjectAsCSV(titles, visionProductConfig)
    return visionProductContent


def getDetailedData(productSummary):
    for product in productSummary:
        paramsDetail = {'id': productSummary['id']}
        resp = requests.get(summaryListUrl, paramsDetail)
        exportObjectAsCSV(None, None)
    return 0




def parseResponseAsJson():
    pass


def exportObjectAsCSV(titles, data):
    print(titles)
    for index, line in enumerate(data):
        print('Line', index + 1, ':', line)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    productSummary = getSummaryData()
    getDetailedData(productSummary)
