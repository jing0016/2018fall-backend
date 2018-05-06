import json
import requests
import sys
import math

def colDiscount(discount_id,collection_type,discount_value,url):
    URL = url.format(discount_id,1)
    r = requests.get(URL)
    j = r.json()
    total_page_number = math.ceil(j["pagination"]["total"]/j["pagination"]["per_page"])

    total_amount = 0

    total_after_discount =0

    for product in j["products"]:
        total_amount += product["price"]
        total_after_discount += product["price"]
        if "collection" in product:
            if product["collection"] == collection_type:
                if (product["price"] - discount_value) >= 0:
                    total_after_discount -= discount_value

                else:
                    total_after_discount -= product["price"]


    current_page_number = 2

    while current_page_number <= total_page_number:
        URL = url.format(discount_id, current_page_number)
        r = requests.get(URL)
        j = r.json()

        for product in j["products"]:
            total_amount += product["price"]
            total_after_discount += product["price"]
            if "collection" in product:
                if product["collection"] == collection_type:
                    if (product["price"] - discount_value) >= 0:
                        total_after_discount -= discount_value
                    else:
                        total_after_discount -= product["price"]


        current_page_number += 1

    return { "total_amount": total_amount, "total_after_discount": total_after_discount }

def proDiscount(discount_id,discount_value,product_value,url):
    URL = url.format(discount_id, 1)
    r = requests.get(URL)
    j = r.json()
    total_page_number = math.ceil(j["pagination"]["total"] / j["pagination"]["per_page"])

    total_amount = 0

    total_after_discount = 0

    for product in j["products"]:
        total_amount += product["price"]
        total_after_discount += product["price"]
        if product["price"] >= product_value:
            if (product["price"] - discount_value) >= 0:
                total_after_discount -= discount_value
            else:
                total_after_discount -= product["price"]

    current_page_number = 2

    while current_page_number <= total_page_number:
        URL = url.format(discount_id, current_page_number)
        r = requests.get(URL)
        j = r.json()

        for product in j["products"]:
            total_amount += product["price"]
            total_after_discount += product["price"]
            if product["price"] >= product_value:
                if (product["price"] - discount_value) >= 0:
                    total_after_discount -= discount_value
                else:
                    total_after_discount -= product["price"]
        current_page_number += 1

    return { "total_amount": total_amount, "total_after_discount": total_after_discount }

def cartDiscount(discount_id,discount_value,cart_value,url):
    URL = url.format(discount_id, 1)
    r = requests.get(URL)
    j = r.json()
    total_page_number = math.ceil(j["pagination"]["total"] / j["pagination"]["per_page"])

    total_amount = 0

    total_after_discount = 0

    for product in j["products"]:
        total_amount += product["price"]

    current_page_number = 2

    while current_page_number <= total_page_number:
        URL = url.format(discount_id, current_page_number)
        r = requests.get(URL)
        j = r.json()

        for product in j["products"]:
            total_amount += product["price"]

        current_page_number += 1

    if total_amount >= cart_value:
        total_after_discount = total_amount - discount_value
    else:
        total_after_discount = total_amount

    return { "total_amount": total_amount, "total_after_discount": total_after_discount }




s = sys.stdin.readline();
d = json.loads(s);

discount_id = d["id"]
discount_type = d["discount_type"]
discount_value = d["discount_value"]

url = "https://backend-challenge-fall-2018.herokuapp.com/carts.json?id={}&page={}"

if(list(d.keys())[-1]=="collection"):
    collection_type = d["collection"]
    str = colDiscount(discount_id,collection_type,discount_value,url)
    print(json.dumps(str,indent = 2))
elif (list(d.keys())[-1]=="product_value"):
    product_value = d["product_value"]
    str = proDiscount(discount_id,discount_value,product_value,url)
    print(json.dumps(str, indent=2))
else:
    cart_value = d["cart_value"]
    str = cartDiscount(discount_id,discount_value,cart_value,url)
    print(json.dumps(str, indent=2))