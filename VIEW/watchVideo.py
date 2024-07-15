import threading
import logging
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from FileHandler import FileHandler
import time

logging.basicConfig(level=logging.INFO)


class VideoBot:
    def __init__(self, file_handler):
        """
        Initialize VideoBot.

        Parameters:
        - file_handler: FileHandler instance.
        """
        self.file_handler = file_handler

    def open_chrome(self, proxy):
        """
        Open Chrome browser with specified proxy.

        Parameters:
        - proxy (str): Proxy URL.

        Returns:
        - driver: Selenium WebDriver instance.
        """
        try:
            driver = Driver(uc=True, incognito=True, proxy=proxy, undetectable=True, headless=False)#uc=True,uc=True,
            print('driver ')
            return driver
        except Exception as e:
            logging.error(f"Error opening Chrome: {e}")
            if driver:
                driver.quit()
            raise

    def fetch_video_from_blog_post(self, driver, blog_post_1_link, blog_post_2_link, video_url, thread_number):
        """
        Fetch video link from a series of blog posts.

        Parameters:
        - driver: Selenium WebDriver instance.
        - blog_post_1_link (str): Link to the first blog post.
        - blog_post_2_link (str): Link to the second blog post.
        - video_url (str): Link to the video.
        - thread_number (int): Thread number for logging.
        """
        try:
            driver.uc_open(video_url)
            driver.maximize_window()
            logging.info(f"Thread number{thread_number}: Blog post 1 opened")
            time.sleep(5)
            # driver.click_link(blog_post_2_link, timeout=30)
            # logging.info(f"Thread number{thread_number}: Blog post 2 opened")
            # time.sleep(5)
            driver.click_link(blog_post_1_link, timeout=30)
            logging.info(f"Thread number{thread_number}: Video link opened")

        except Exception as e:
            logging.error(f"Thread number:{thread_number} Error redirecting to video: {e}")
            raise

    def watch_video(self, driver, video_url, watchDuration, thread_number):
        """
        Watch a video and interact with ads.

        Parameters:
        - driver: Selenium WebDriver instance.
        - video_url (str): Link to the video.
        - watch_duration (int): Duration to watch the video.
        - thread_number (int): Thread number for logging.
        """
        try:
            driver.uc_open(video_url)
            logging.info(f"Thread number:{thread_number} Watching video at {video_url} for {watchDuration} seconds.")
            time.sleep(watchDuration)
        except Exception as e:
            logging.error(f"Thread number:{thread_number} Error opening video: {e}")
            raise

    def login_gmail(self, driver, email, password, recovery_email, thread_number):
        """
        Log in to Gmail.

        Parameters:
        - driver: Selenium WebDriver instance.
        - email (str): Gmail email address.
        - password (str): Gmail password.
        - recovery_email (str): Recovery email address.
        - thread_number (int): Thread number for logging.
        """
        try:
            driver.maximize_window()
            driver.uc_open("https://accounts.google.com/signin")
            driver.sleep(5)
            driver.type('input[id="identifierId"]', email, timeout=20)
            driver.uc_click('div[id="identifierNext"]', by=By.CSS_SELECTOR, timeout=20)
            logging.info(f"Thread number:{thread_number} Email next clicked")
            driver.type('input[name="Passwd"]', password, timeout=20)
            driver.uc_click('div[id="passwordNext"]', by=By.CSS_SELECTOR, timeout=20)
            logging.info(f"Thread number:{thread_number} Password next clicked")
            try:
                driver.uc_click('#yDmH0d > c-wiz > div > div.eKnrVb > div > div.j663ec > div > form > span > section:nth-child(2) > div > div > section > div > div > div > ul > li:nth-child(3) > div > div.vxx8jf', by=By.CSS_SELECTOR, timeout=20)
                logging.info(f"Thread number:{thread_number} Recovery button clicked")
                driver.type('#knowledge-preregistered-email-response', recovery_email, timeout=20)
                driver.uc_click('#view_container > div > div > div.pwWryf.bxPAYd > div > div.zQJV3 > div > div.qhFLie > div > div > button', by=By.CSS_SELECTOR, timeout=20)
                logging.info(f"Thread number:{thread_number} Recovery Next button clicked")
            except Exception as e:
                logging.error(f"Thread number:{thread_number} An error occurred during recovery")

            logging.info(f"Thread number:{thread_number} Log in successful!!!!!!!!")
        except Exception as e:
            logging.error(f"Thread number:{thread_number} An error occurred during login: {e}")

    def bot_task(self, thread_number, video_url, watchDuration, blog1, blog2, proxy=None):
        """
        Perform bot tasks: login, fetch video, watch video.

        Parameters:
        - thread_number (int): Thread number for logging.
        - video_url (str): Link to the video.
        - watch_duration (int): Duration to watch the video.
        - email (str): Gmail email address.
        - password (str): Gmail password.
        - recovery_email (str): Recovery email address.
        - proxy (str): Proxy URL.
        """
        driver = None
        try:
            driver = self.open_chrome(proxy)
        #    if email and password:
         #       self.login_gmail(driver, email, password, recovery_email, thread_number)
            self.fetch_video_from_blog_post(driver, blog1, blog2, video_url, thread_number)
            self.watch_video(driver, blog1, watchDuration, thread_number)
        except Exception as e:
            logging.error(f"Thread number:{thread_number} Bot task failed: {e}")
            driver.quit()
        finally:
            if driver:
                logging.info(f"Closing thread number:{thread_number + 1}. Bot task Successfull!")
                driver.quit()


# Function to run bot threads 
def run_bot_threads(video_bot, video_url, watchDuration, num_views, num_threads=1,
                    proxies_list=None, blog1=None, blog2=None):
    """
    Run multiple bot threads.

    Parameters:
    - video_bot: VideoBot instance.
    - video_url (str): Link to the video.
    - watch_duration (int): Duration to watch the video.
    - num_views (int): Total number of views.
    - num_threads (int): Number of threads.
    - login_credentials_list (list): List of login credentials.
    - proxies_list (list): List of proxy URLs.
    """
    threads = []
    try:
        for i in range(num_views // num_threads):
            for j in range(num_threads):
          #      email, password, recovery_email = video_bot.file_handler.select_random_login_credentials(
           #         login_credentials_list)
                proxy_url = video_bot.file_handler.select_random_proxy(proxies_list)
                thread_number = i * num_threads + j
                time.sleep(5)
                thread = threading.Thread(target=video_bot.bot_task,
                                          args=(thread_number, blog1, watchDuration, video_url, blog2, proxy_url))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
    except Exception as e:
        logging.error(f"Error creating threads: {e}")
