#####################
#### This script sends HTTP calls to fetch the data from websites and parses the data as JSON objects
#### Copyright: SoGoo International GmbH
#####################

import requests
import csv

baseUrl = 'https://www.hikrobotics.com'
summaryListUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductContent?'
detailUrl = baseUrl + '/en/Api/Foreground/Vision/VisionProductConfig?'


def getSummaryData(firstModuleId, secondaryModuleId, page): # 1 file, 29 lines
    paramsSummary = {'firstModuleId': firstModuleId, 'page': page, 'secondaryModuleId': secondaryModuleId, 'size': 100, 'screening': None}
    resp = requests.get(summaryListUrl, paramsSummary)
    data = resp.json()
    visionProductConfig = data['data']['VisionProductConfig'] # list, len = 29
    visionProductContent = data['data']['VisionProductContent']['records'] # list, len = 29
    # make sure that the title list and the data have the same dimension
    titleList = ['id', 'productModel', 'Sensor', 'Resolution', 'Max. Frame Rate', 'Data Interface', 'Mono/Color']
    dataList = []
    for productConfig in visionProductConfig:
        dataDict = {}
        for i in range(len(titleList)):
            if i < 2:
                dataDict[titleList[i]] = visionProductContent[i][titleList[i]]
            else:
                dataDict[titleList[i]] = productConfig[i - 2]
        dataList.append(dataDict)
    print('Now exporting summary(table) data as CSV file')
    exportObjectAsCSV(titleList, dataList, 'Table', True)
    return visionProductContent


def getDetailedData(productSummary): # 29 files, each file has 33 columns -> each dict creates a file
    titleList = []
    dataList = []
    for productIdx, product in enumerate(productSummary):
        print('Now fetching detailed data, please wait. Progress: ', productIdx + 1, '/', len(productSummary))
        dataDict = {}
        paramsDetail = {'id': product['id']}
        respData = requests.get(detailUrl, paramsDetail).json()['data']
        if len(respData) > 0:
            for respLine in respData:
                if productIdx == 0:
                    titleList.append(respLine['name'])
                dataDict[respLine['name']] = respLine['value']
            dataList.append(dataDict)
    print('Now exporting detailed data as CSV file')
    exportObjectAsCSV(titleList, dataList, 'Detail', True)
    print('Successfully fetched all Hikrobot data!')



def exportObjectAsCSV(titles, dataList, filePattern, onlyOneFile=False):
    """
    :param titles: List
    :param data:  List -> a dataList can have multiple dicts. Each dict generates a file
    """
    print(titles)
    if onlyOneFile:
        with open('c:\\hikdata\\' + filePattern + '.csv', mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(titles)
            for index, data in enumerate(dataList):
                csv_writer.writerow(list(data.values()))
    else:
        for index, data in enumerate(dataList):
            with open('c:\\hikdata\\' + str(index) + '-' + filePattern + '.csv', mode='w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(titles)
                csv_writer.writerow(list(data.values()))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    productSummary = getSummaryData(78, 42, 1)
    getDetailedData(productSummary)
