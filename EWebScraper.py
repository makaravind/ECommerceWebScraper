"""
    using Beautifull soup and requests module
    searchs the input keyword and prints out top 10 results from Amazon and Ebay
    calculates the time from the request to end printiing results

"""
# todo use threads
# todo GUI

from bs4 import BeautifulSoup
import requests
import string
import time

def Removewords(tag):
    '''
    :param words:  arguments from the getopt
    :return: remove digits from all the words : CleanWords
    '''
    CleanWord = [letter for letter in tag if letter in string.digits or letter == "."]
    return "".join(CleanWord)

def GetEbayItems(soup):

    final = {}
    results = soup.find_all("div",{"id":"ResultSetItems"})
    result_items =  results[0].find_all("li",{"class":"sresult"})
    for item_count,item in enumerate(result_items,1):
        item_name =  str(item.find_all("h3",{"class":"lvtitle"})[0].next.get('title')[25:])#.next.next
        item_price = item.find_all("ul",{"class":"lvprices"})[0].next.next
        item_price_striped =  item_price.find_all("span",{"class":"bold"})[0]
        item_price_striped = Removewords(str(item_price_striped))
        final.__setitem__(item_name,item_price_striped)
        if item_count == 10 :
            break
    return final


######################################################################


def GetAmazonitems(soup):

    final = {}
    results = soup.find("div",{"id":"atfResults"})
    try:
        result_items = results.next.find_all("li")
        for item_count,item in enumerate(result_items,1):
            item_name =  item.find("div",{"class":"s-item-container"}).next.next.find_all("div",{"class":"a-row"})[2].next.string
            item_price =  item.find("div",{"class":"s-item-container"}).next.next.find_all("div",{"class":"a-row"})[4]\
                .find("span",{"class":"a-size-base a-color-price s-price a-text-bold"})
            item_price = Removewords(str(item_price))
            final.__setitem__(item_name,item_price)
            if item_count == 10: break
    except AttributeError as Ae:
        pass
    return final

def Main():

    search  = raw_input("enter the search item:")
    ebay_link = "http://www.ebay.in/sch/i.html?_from=R40&_trksid=p2050601.m570.l1313.TR10.TRC0.A0.H0.X"+search+".TRS0&_nkw="+search+"&_sacat=0"
    amazon_link = "https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+search

    start = time.time()
    print "got your search keyword..."
    # creating requesting , soup , getting result
    ebay = requests.get(ebay_link)
    ebay_soup = BeautifulSoup(ebay.content,"html.parser")
    print "request succesfull.."
    exception_counter_e = 1
    try:
        Ebay_Items = GetEbayItems(ebay_soup)
    except:
        exception_counter_e += 1
        if exception_counter_e == 5 :
            Ebay_Items = GetEbayItems(ebay_soup)
        else: "can't get results from ebay.."
    print "got your items from ebay..."

    # creating requesting ,soup , getting result
    amazon = requests.get(amazon_link)
    amazon_soup = BeautifulSoup(amazon.content,"html.parser")
    print("request sucessfull..")
    exception_counter = 1
    try:
        Amazon_Items = GetAmazonitems(amazon_soup)
    except:
        exception_counter+=1
        if exception_counter != 5 :
            Amazon_Items = GetAmazonitems(amazon_soup)
        else: "can't get reaults from Amazon"
    print "got your items from amazon..."


    print('\n'* 50) # clearing the screen
    # printing the acquried results
    print "----------------EBAY DEALS---------------"
    for key, value in Ebay_Items.iteritems():
        print key,"---------------------------------------------------------->","RS", value
    print "\n"
    print "----------------AMAZON DEALS---------------"
    for key, value in Amazon_Items.iteritems():
        print key ,"---------------------------------------------------------->","RS.",

    end = time.time()
    print "results in "+str(end-start)+"secs..."

Main()
