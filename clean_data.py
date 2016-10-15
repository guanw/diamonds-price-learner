from bs4 import BeautifulSoup
import csv
import os

def getShape(soup):
    interested_div = soup.findAll("span", {"data-classes": "diamond-shape-sprite shape cell compressible shape cell compressible"})
    shape_list = []
    for item in interested_div:
        shape_list.append(item['data-uncompressed-value'])
    return shape_list

def getAttribute(soup, attribute):
    if attribute == "carat":
        interested_div = soup.findAll("span", {"class": "carat cell carat cell"})
    elif attribute == "cut":
        interested_div = soup.findAll("span", {"class": "cut cell cut cell"})
    elif attribute == "color":
        interested_div = soup.findAll("span", {"class": "color cell color cell"})
    elif attribute == "clarity":
        interested_div = soup.findAll("span", {"class": "clarity cell clarity cell"})
    elif attribute == "price":
        interested_div = soup.findAll("span", {"class": "pricePerCarat cell advanced pricePerCarat cell advanced"})
    attribute_res = []
    for item in interested_div:
        attribute_res.append(item.text)
    return attribute_res

def get_data_row(soup):
    interested_div = soup.findAll("div",{"class": "row data-row"})
    print interested_div[:5]

def decode_price(str):
    return int(str[1] + str[3:])
def decode_unicode_string(str):
    return str.encode("ascii")
def decode_carat(str):
    return float(str)

def decompose_filename(filename):
    index = filename.find('.')
    start = int(filename[:index])
    end = start + 99
    return (start,end)

def filter_price_range(filename, complex_list):
    # print "filter " + filename
    (start, end) = decompose_filename(filename)
    res = []
    for complex in complex_list:
        price = complex.price * 1.0 * complex.carat
        if price >= start and price <= end:
            complex.price = price
            res.append(complex)
    return res

class complex:
    def __init__(self, shape, carat, cut, color, clarity, price):
        self.shape = shape
        self.carat = carat
        self.cut = cut
        self.color = color
        self.clarity = clarity
        self.price = price

def decoding_cleaning(lis, attribute):
    res = []
    if attribute == "price":
        for str in lis:
            res.append(decode_price(str))
    elif attribute == "carat":
        for str in lis:
            res.append(decode_carat(str))
    else:
        for str in lis:
            res.append(decode_unicode_string(str))
    return res

def compose_complex(soup):
    shape_list = getShape(soup)
    carat_list = getAttribute(soup, "carat")
    cut_list = getAttribute(soup, "cut")
    color_list = getAttribute(soup, "color")
    clarity_list = getAttribute(soup, "clarity")
    price_list = getAttribute(soup, "price")

    shape_list = decoding_cleaning(shape_list, 'shape')
    carat_list = decoding_cleaning(carat_list, 'carat')
    cut_list = decoding_cleaning(cut_list, 'cut')
    color_list = decoding_cleaning(color_list, 'color')
    clarity_list = decoding_cleaning(clarity_list, 'clarity')
    price_list = decoding_cleaning(price_list, 'price')

    complex_list = []
    for i in range(len(price_list)):
        complex_list.append(complex(shape_list[i], carat_list[i], cut_list[i], color_list[i], clarity_list[i], price_list[i]))

    return complex_list

def clear_data():
    file_folders = ['Emerald','Oval','Round']
    with open('data.csv','wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for folder in file_folders:
            file_names = os.listdir("./html/" + folder)
            for file in file_names:
                html = open("./html/" + folder + "/" + file, "r").read()
                soup = BeautifulSoup(html)
                complex_list = compose_complex(soup)
                complex_list = filter_price_range(file, complex_list)

                for complex in complex_list:
                    writer.writerow([complex.shape, str(complex.carat), complex.cut, complex.color, complex.clarity, str(complex.price)])



if __name__ == "__main__":
    clear_data()