from PIL import Image
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from definitions import MEDIA_URL
from logger import Logger
import time


def store_post_images(url: str) -> None:
    """
    Stores a set of images for a given post in Reddit.
    :param url: The url to the post.
    """
    Logger.info(f"Entering {store_post_images.__name__} to retrieve images from {url}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    Logger.info(f"Attempting to remove cookies etc...")

    wait_for_element(driver=driver,
                     xpath='//*[@id="AppRouter-main-content"]/div/div[1]/div/div/div[2]/button',
                     click=True)

    wait_for_element(driver=driver,
                     xpath='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]'
                           '/div[1]/div/div[5]/div/div',
                     click=True)

    Logger.info("Attempting to collect title and comments from: {url}")

    title = wait_for_element(driver=driver,
                             xpath='/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]')
    set_window_focus(driver, title, f"{MEDIA_URL}\\Images\\title.png")
    comments = wait_for_element(driver=driver,
                                xpath='//div[@style="padding-left:16px"]',
                                multiple=True)
    [set_window_focus(driver, comment, f"{MEDIA_URL}\\Images\\{index}.png")
        for index, comment
        in enumerate(comments[:3])]

    Logger.info(f"Saved images for {store_post_images.__name__}; Returning...")

    driver.quit()


def wait_for_element(driver: webdriver, xpath: str, click=False, multiple=False):
    """
    Waits for a webdriver element and throws non-fatal error if it cannot be found.
    :param driver: The webdriver.
    :param xpath: The xpath to the desired element.
    :param click: Whether or not the element should be clicked.
    :param multiple: Whether or not there are multiple elements.
    :return None if the element cannot be found or should be clicked; The element if it does not need to be clicked.
    """
    Logger.info(f"Entering {wait_for_element.__name__}")
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))) if not multiple \
            else WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        
        Logger.info(f"Successfully found element with XPATH: {xpath}")

        return element if not click else element.click()

    except NoSuchElementException and TimeoutException:
        Logger.warning(f"Could not find an element with the XPATH: {xpath}.")
        return None


def set_window_focus(driver: webdriver, element: WebElement, path: str) -> None:
    """
    Sets the window focus on the webpage to take an image of a given comment.
    :param driver: The webdriver.
    :param element: The element to scope to.
    :param path: The path to the saved image.
    """
    Logger.info(f"Entering {set_window_focus.__name__}")

    x, y = element.location.values()
    height, width = element.size.values()

    # 49px accounts for the navigation bar in reddit
    driver.execute_script(f"window.scrollTo(0, {y - 49})")

    # Let the data render on the webpage
    time.sleep(1)
    driver.save_screenshot(path)

    Logger.info(f"Unformatted image has been saved.")
    
    crop_focused_area_and_save(x, width, height, path)


def crop_focused_area_and_save(x: int, width: int, height: int, path: str) -> None:
    """
    Crops the image to the desired focus area.
    :param x: The x pos.
    :param width: The width of the area.
    :param height: The height of the area.
    :param path: The path to the image to be cropped.
    """
    Logger.info(f"Entering {crop_focused_area_and_save.__name__}")
    Logger.info(f"Attempting to crop and resize the image...")

    image: Image = Image.open(path)
    crop_rectangle: tuple(int, int, int, int) = (x, 49, width + x, height + 49)
    cropped_image: Image = image.crop(crop_rectangle)
    image_width: int = cropped_image.width
    change_percentage = 1080 / image_width
    resized_image = cropped_image.resize((1080, int(cropped_image.height * change_percentage)))

    Logger.info(f"Successfully cropped and resized image, attempting to save to: {path}")

    resized_image.save(path)

    Logger.info(f"Image has been saved.")


