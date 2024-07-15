# runBot.py

from FileHandler import FileHandler
from watchVideo import VideoBot, run_bot_threads

def get_hardcoded_params():
    """
    Get hardcoded parameters from user input.

    Returns:
    - Tuple of parameters.
    """
    proxies_file_path = 'proxies.xlsx'
    #login_credentials_file_path = 'C:/Users/extractdata/Desktop/automation/logins.xlsx'
    video_url = 'https://www.youtube.com/watch?v=i4tOTmRcELE'
    blog1 = 'https://test24124-4.blogspot.com/2023/12/can-do-like-blogger-to-blogger-like.html'# < -- this is the blog post which it is watching now.
    blog2 = 'https://test24124-4.blogspot.com/2023/11/title-unleashing-potential.html'

    num_views = int(input("Enter the total number of views: "))
    num_threads = int(input("Enter the number of threads: "))
    watch_duration = int(input("Enter watch duration in seconds: "))

    return proxies_file_path, video_url, num_views, num_threads, watch_duration, blog1, blog2

if __name__ == "__main__":
    proxies_file_path, video_url, num_views, num_threads, watch_duration, blog1, blog2 = get_hardcoded_params()

    file_handler = FileHandler(proxies_file_path, None)
    video_bot = VideoBot(file_handler)

 #   login_credentials_list = file_handler.read_login_credentials_from_excel(
  #      email_col_index=0,
   #     password_col_index=1,
    #    recovery_email_col_index=2
    #)
    proxies_list = file_handler.read_proxies_from_excel(ip_col_index=0, port_col_index=1)
    proxies_list = []
    run_bot_threads(video_bot, blog1, watch_duration, num_views, num_threads, proxies_list, video_url, blog2)

# End of runBot.py
