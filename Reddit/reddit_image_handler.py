from dataclasses import dataclass
from PIL import Image
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class ScreenDimensions:
    x: int
    y: int
    width: int
    height: int


def store_web_image(url: str) -> None:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    wait_for_element(driver=driver,
                     xpath='//*[@id="AppRouter-main-content"]/div/div[1]/div/div/div[2]/button',
                     click=True)

    wait_for_element(driver=driver,
                     xpath='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]'
                           '/div[1]/div/div[5]/div/div',
                     click=True)

    title = wait_for_element(driver=driver,
                             xpath='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]')

    set_window_focus(driver, title, "test.png")
    driver.quit()


def wait_for_element(driver: webdriver, xpath: str, click=False) -> WebElement:
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))

        return element if not click else element.click()

    except NoSuchElementException and TimeoutException:
        print(f"Could not find an element with the XPATH: {xpath}.")

        return None


def set_window_focus(driver: webdriver, element: WebElement, path: str) -> None:
    x, y = element.location.values()
    height, width = element.size.values()
    driver.save_screenshot(path)
    crop_focused_area(x, y, width, height, path)


def crop_focused_area(x, y, width, height, path):
    image = Image.open(path)
    crop_rectangle = (x, y, width + x, height + y)
    cropped_image = image.crop(crop_rectangle)
    cropped_image.save(path)


