from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os

def click_shape(driver, shape):
    input = driver.find_element_by_xpath("//label[@title='" + shape + "']")
    input.click()

    sleep(2)
    return

def change_input_value(driver, current_min, current_max, attribute):
    min_input = driver.find_element_by_id(attribute + "-selector-text-min")
    max_input = driver.find_element_by_id(attribute + "-selector-text-max")

    min_input.clear()
    min_input.send_keys(current_min)
    sleep(2)

    max_input.clear()
    max_input.send_keys(current_max)
    sleep(2)
    return



def change_slider_value(driver, attribute):

    slidebar = driver.find_element_by_id(attribute + "-selector")
    width = slidebar.size['width']

    # slidebar_spans = driver.find_elements_by_class_name("diamond-search-value-mark")
    slidebar_spans = driver.find_elements_by_xpath("//div[@id='" + attribute + "-selector']/span[@class='diamond-search-hashmark']")
    if len(slidebar_spans) + 1 < 4 and attribute == "cut":
        return
    elif len(slidebar_spans) + 1 < 7 and attribute == "color":
        return
    elif len(slidebar_spans) + 1 < 8 and attribute == "clarity":
        return

    move_min_slider = webdriver.ActionChains(driver);
    move_max_slider = webdriver.ActionChains(driver);



    min_slider = driver.find_element_by_xpath("//div[@id='" + attribute + "-selector']/a[1]")
    max_slider = driver.find_element_by_xpath("//div[@id='" + attribute + "-selector']/a[2]")




    if attribute == "cut":
        min_offset = width/4
        max_offset = -width/4

    elif attribute == "color":
        min_offset = width*3/7
        max_offset = -width/7

    elif attribute == "clarity":
        min_offset = width/2
        max_offset = -width/4


    move_min_slider.click_and_hold(min_slider).move_by_offset(min_offset, 0).release().perform()
    move_max_slider.click_and_hold(max_slider).move_by_offset(max_offset, 0).release().perform()
    sleep(8)


def process_all():
    driver = webdriver.Chrome('/Users/JudeWang/Documents/diamonds-price-learner/chrome-driver/chromedriver')
    driver.get("http://www.bluenile.com/build-your-own-ring/diamonds?elem=head&track=main1")
    list_price = []
    change_input_value(driver, current_min="0.25", current_max="1", attribute="carat")
    change_slider_value(driver, attribute="color")
    change_slider_value(driver, attribute="cut")
    change_slider_value(driver, attribute="clarity")

    for i in range(30):
        list_price.append( (i * 100 + 1000, (i+1) * 100 + 1000))


    for shape in ['Emerald', 'Round', 'Oval']:
        if shape == "Emerald":
            click_shape(driver, "Round")
            click_shape(driver, "Emerald")
        elif shape == "Round":
            click_shape(driver, "Emerald")
            click_shape(driver, "Round")
        else:
            click_shape(driver, "Round")
            click_shape(driver, "Oval")


        for pair in list_price:
            change_input_value(driver, current_min=str(pair[0]), current_max=str(pair[1]), attribute="price")

            div = copy_list_data(driver)
            store_file(div, shape, pair)
            print "finish writing " + str(pair[0]) + ".html file"

    driver.close()
def store_file(div, shape, pair):
    if not os.path.exists('./html/web-crawler/' + shape):
        os.makedirs('./html/web-crawler/' + shape)
    with open('./html/web-crawler/' + shape + '/' + str(pair[0]) + '.html', 'w') as f:
        # f.write(div.contents)
        final_str_content = "".join(str(item) for item in div.contents)
        f.write(final_str_content)
    return


def copy_list_data(driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source)
    div = soup.find('div', {"class": "diamond-grid-container"})
    # print div
    return div


if __name__ == "__main__":
    process_all()
