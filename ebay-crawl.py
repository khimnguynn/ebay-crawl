from requests import Session
import re

token = open("token.txt", encoding="utf-8").read()

def Get_Word():
    ses = Session()
    res = ses.get("https://ydr-api.yourdictionary.com/words/random?limit=1&starts_with=&ends_with=").json()
    return res["data"][0]["headword"]

def Get_ListingId(word):
    cancel = 0

    ses  = Session()
    ses.headers.update({
        "Host": "apisd.ebay.com",
        "X-EBAY-4PP": "AQADiqNchlZ09Rk/nt4lKBX1RnKhouFTLZHFNLbUgaAMp8+nniZvWvmzuuD+YpHwKgYz",
        "X-EBAY-C-ENDUSERCTX": "deviceId=17ab091795c.a9bd6ca.7e396.fffdd928,deviceIdType=IDREF,userAgent=ebayUserAgent/eBayIOS;6.33.0;iOS;15.0.2;Apple;iPhone11_6;Viettel;414x896;3.0",
        "Authorization": str(token).strip(),
        "X-EBAY-C-MARKETPLACE-ID": "EBAY-US",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate, br",
        "X-EBAY-C-TERRITORY-ID": "VN",
        "User-Agent": "eBayiPhone/6.33.0",
        "X-EBAY-C-CORRELATION-SESSION": "devicetimestamp=2021-10-25T15:32:27.703Z,si=b091661217ae1cab1c1d6d40015c15df",
        "Connection": "keep-alive",
        "X-EBAY-C-EXP": "c=5,v=v2,eprlogid=t6fuuq%60%3F%3Cumjcwpse*dsdcp%28rbpv6702-17cb8136c13-0xee,epcalenv=,noepheader=1",
        "ebay-ets-device-theme": "dark",
        "X-EBAY-C-CULTURAL-PREF": "Currency=VND,Timezone=Asia/Ho_Chi_Minh,Units=Metric"
})
    url =f"https://apisd.ebay.com/experience/search/v1/search_results?answersVersion=1&_pgn=1&async=false&_nkw={word}&_sop=12"
    res = ses.get(url).text
    total_Pages = re.findall('totalPages":([^,]+)', res)[0]
    print(f"found {str(total_Pages)} pages")
    listingId = re.findall('"listingId":"([^"]+)', res)
    print(f"keyword: {word} page 1/{str(total_Pages)} found {str(len(listingId))} listingID")
    for i in listingId:
        open("ListingID.txt", "a").write(f"{i}\n")
    if int(total_Pages) == 1:
        return
    else:
        pass
    for i in range(2, int(total_Pages) + 1):
        url =f"https://apisd.ebay.com/experience/search/v1/search_results?answersVersion=1&_pgn={str(i)}&async=false&_nkw={word}&_sop=12"
        res = ses.get(url).text
        listingId = re.findall('"listingId":"([^"]+)', res)
        if len(listingId) == 0:
            cancel += 1
        else:
            cancel = 0
        if cancel == 5:
            return
        else:
            pass
        print(f"keyword: {word} page {str(i)}/{str(total_Pages)} found {str(len(listingId))} listingID")
        for i in listingId:
            open("ListingID.txt", "a").write(f"{i}\n")


if __name__ == "__main__":
    while 1:
        word = Get_Word()
        Get_ListingId(word)

