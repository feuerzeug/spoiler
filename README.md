# spoiler
To test:
Open a python shell

from spoiler import *
user_set = build_test_set()
(Feel free to change num_users, num_series and num_episodes to a smaller/larger number. Also, build_test_set_sparse() builds a more realistic test set where each user only watches about a quarter of the series)

spoiler_set = find_spoilers(user_set)

user_list = list(user_set)
series_list = list(user_list[0].get_series())
lunchmates = find_lunchmates(user_list[0],series_list[0])
