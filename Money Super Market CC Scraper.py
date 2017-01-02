import urllib.request, urllib.parse, urllib.error, re, time, csv

#####Load Create Functions
def get_First(array, default=None):
    if len(array) >  0:
        return array[0]
    else:
        return default

#####
def get_current_table():
    url = 'http://www.moneysupermarket.com/credit-cards/balance-transfer/'
    regex = '<li class=\"creditcard(.*?)</li>' #the string in the parentheses is the target of the find all
    pattern = re.compile(regex)
    htmlfile = urllib.request.urlopen(url)
    htmltext = htmlfile.read().decode(encoding='utf_8')
    cards = re.findall(pattern,htmltext)
    i=0
    while i<len(cards) :
        cards[i] = cards[i]+'\">'
        i+=1

    current_table = []
    i=0
    while i<len(cards) :
        search_time = time.asctime((time.localtime(time.time())))
        position = i+1
        card_name = re.findall(re.compile('data-productcode=\"(.*?)\"'),cards[i])
        bt_cost = re.findall(re.compile('data-total-cost=\"(.*?)\"'),cards[i])
        bt_period = re.findall(re.compile('data-interest-free-period=\"(.*?)\"'),cards[i])
        product = re.findall(re.compile('data-productname=\"(.*?)\"'),cards[i])
        provider = re.findall(re.compile('data-providername=\"(.*?)\"'),cards[i])
        fee = re.findall(re.compile('<span data-productattribute=\"balanceTransferHandlingFee\"> <strong>(.*?)</strong>'),cards[i])
        if ('limited-offer' in (cards[i][:15])) : limited_offer_flag = 1
        else: limited_offer_flag = 0
        data = [search_time,position,get_First(provider,'Error:No Provider Found'),get_First(product,'Error:No Product Found'),get_First(bt_period,'Error:No BT Period Found'),get_First(fee, 'Error:No fee found'),get_First(bt_cost,'Error:No BT Cost Found'),limited_offer_flag]
        current_table.append(data)
        i+=1
    return current_table

#####
def get_last_table():
    incards = []
    with open('MSMTable.csv') as csvinput:
        readCSV = csv.reader(csvinput, delimiter=',')
        for row in readCSV:
            incards.append(row)
            lastrow = row
    last_table = []
    i=0
    while i<len(incards) :
        if incards[i][0][:11] == lastrow[0][:11] : last_table.append(incards[i])
        i+=1
    return last_table
    
#####
def write_to_file(output):
    with open('MSMTable.csv', 'a', newline='') as csvoutput:
            outputwriter = csv.writer(csvoutput, delimiter=',')
            outputwriter.writerows(output)
            csvoutput.close()


###Start of Script
current_table = get_current_table()
last_table = get_last_table()
write_to_file(current_table)







        
