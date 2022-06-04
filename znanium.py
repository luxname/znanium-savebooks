import pickle, os, time, base64, sys, img2pdf, shutil
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


from selenium.webdriver.firefox.service import Service

import re
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


ser = Service('./geckodriver')
# Hardcoding names of files for an every getting page
list_of_img = ('1.png', '2.png', '3.png', '4.png', '5.png', '6.png')

link = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3]) + 1

# Defines the webdriver and options (useragent and dom.webdriver.enabled)
option = webdriver.FirefoxOptions()
option.set_preference("general.useragent.override", 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/92.0')
option.headless = True
browser = webdriver.Firefox(service=ser,options=option)

# Get cookies
def get_cookies ():
    with open ('auth.txt', 'r') as file:
        data = file.readline().split()
    browser.get('https://znanium.com')
    browser.find_element(by=By.XPATH, value='/html/body/header/div/div/div/div/a[2]').click()
    browser.find_element(by=By.XPATH, value='//*[@id="loginform-username"]').send_keys(f'{data[0]}')
    browser.find_element(by=By.XPATH, value='//*[@id="loginform-password"]').send_keys(f'{data[1]}')
    browser.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div[2]/div/div/div[2]/form/div[4]/button').click()
    try:
        browser.find_element(by=By.XPATH, value='//*[@id="w1-error-0"]')
        browser.quit()
        sys.exit('Cookies didn\'t received. Try to wait 5 minutes or more. Then try again')
    except NoSuchElementException:
        time.sleep(3)
        pickle.dump(browser.get_cookies(), open('session','wb'))
        print ('Cookies successfully received')

# Enter cookies into the webdriver
def enter_cookies ():
    browser.implicitly_wait(20) # Set the maximum waiting time for an page to appear
    browser.get(link)
    for cookie in pickle.load(open('session', 'rb')):
        browser.add_cookie(cookie)
    browser.refresh()
    print ('Cookies was entered')

# Zoom out for less waiting time to visible of elements of page of book
def zoom_out ():
    for _ in range (3):
        browser.find_element(by=By.XPATH, value='//*[@id="less-icon__off"]').click()

# Making directories in a folder of script
def make_dirs ():
    if not os.path.isdir('book_pages'):
        os.mkdir('book_pages')
    if not os.path.isdir('tmp_img'):
        os.mkdir('tmp_img')
    os.chdir('tmp_img')

# Moving to a particular page
def scroll (page):
    page_field = browser.find_element(by=By.XPATH, value='//*[@id="page"]')
    page_field.clear()
    page_field.send_keys(f'{page}')
    page_field.send_keys(Keys.ENTER)

# Making of a page of boook
def make_page (page):
    scroll(page)
    time.sleep(1.1)
    for i in range(1,7):
        try:
            part_of_page = browser.find_element(By.ID, f'bookreadimg-{page}-{i}').get_attribute('src').replace('data:image/png;base64,', '')
            with open (f'{i}.png', 'wb') as file:
                file.write(base64.b64decode(part_of_page))
        except (NoSuchElementException, StaleElementReferenceException):
            os.chdir('..')
            browser.quit()
            print ('The expected error occurred. The script will be restart and continue from the last loaded page...')
            os.system(f'python {__file__} {link} {page} {end - 1}')
    imgs = [Image.open(img) for img in list_of_img]
    widths, heights = zip(*(img.size for img in imgs))
    total_height = sum(heights)
    max_width = max(widths)
    final_img = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for img in imgs:
        final_img.paste(img, (0, y_offset))
        y_offset += img.size[1]
    final_img.save(f'../tmp_img/page_{page}.png')
    os.rename(f'../tmp_img/page_{page}.png',f'../book_pages/page_{page}.png')
    for img in list_of_img:
        os.remove(img)

# Creating book and delete unnecessary directories
def create_book():
    os.chdir('../book_pages')
    os.rmdir('../tmp_img')
    files = [f for f in os.listdir(os.getcwd()) if f.endswith('.png')]
    pages_to_convert = sorted_alphanumeric(files)
    try:
        with open("../book.pdf","wb") as file:
	        file.write(img2pdf.convert(pages_to_convert))
        os.rename("../book.pdf", "../final_book.pdf")
        os.chdir('..')
        shutil.rmtree('book_pages')
        print ('Book is already')
    except Exception as e:
        print(e)
        pass

def main (link, start, end):
    if not os.path.exists('session'):
        get_cookies()
    enter_cookies()
    make_dirs()
    zoom_out()
    for page in range(start, end):
        if(not os.path.exists(f'../book_pages/page_{page}.png') or os.path.getsize(f'../book_pages/page_{page}.png')<100):
            make_page(page)
        print (f'Page {page} downloaded')
    browser.quit()
    create_book()


if __name__ == '__main__':
    main(link, start, end)
