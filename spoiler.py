import random

   
class episode(object):
    def __init__(self, name=None, user_list=None):
        self._name = name
        self._user_set = set()
    
    def get_name(self):
        return self._name
    
    def get_user_set(self):
        return self._user_set
    
    def add_user(self, user_instance):
        if type(user_instance) != user:
            raise TypeError("is not a user")
        self._user_set.add(user_instance)

    def delete_user(self, user_instance):
        _user_set.remove(user_instance)
        
class user(object): 
    def __init__(self, name):
        self._name = name
        self._series_set = set()

    def __str__(self):
        return "<" + self._name + ", watching " + str(len(self._series_set)) + " series>"
    
    def get_series_set(self):
        return self._series_set
    
    def add_series(self, series_instance):
        if type(series_instance) != series:
            raise TypeError("is not a series")
        self._series_set.add(series_instance)

    def get_name(self):
        return self._name

class series(object):
    def __init__(self, name): # skim optional episodes param
        self._episode_list = []
        self._name = name
    
    def get_name(self):
        return self._name

    def get_episode_list(self):
        return self._episode_list
 
    def add_episode(self, episode_instance):
        if type(episode_instance) != episode:
            raise TypeError("not an episode")
        if episode_instance in self._episode_list:
            raise AssertionError("Episode " + episode_instance + " is already in list")
        self._episode_list.append(episode_instance)

    def user_progress(self, user_instance, episode_instance):
        for _episode in self._episode_list:
            if user_instance in _episode.get_user_list():
                _episode.delete_user(user_instance)
            if _episode == episode_instance:
                _episode.add_user(user_instance)

# builds a test set of users, series and episodes
def build_test_set(num_users=3128, num_series=204, num_episodes=24):
    user_set = set()
    for i in range(0,num_users):
        user_set.add(user('user'+str(i+1)))
    series_set = set()
    for i in range(0,num_series):
        series_ = series('series'+str(i+1))
        for j in range(0,num_episodes):            
            series_.add_episode(episode("episode"+str(j+1)))
        series_set.add(series_)
    for _series in series_set:
        for _user in user_set:
            _user.add_series(_series)
            #_series.add_user(_user) # maybe skip
            _episode_list = _series.get_episode_list()
            _episode_list[random.randint(0,len(_episode_list)-1)].add_user(_user) # only name / id of user instead of object. we already rely on index dict for username -> user object
    #index = {u.get_name() : u for u in user_list}
    #return (user_list, series_list, index)
    return user_set

def build_test_set_sparse(num_users=3128, num_series=204, num_episodes=24):
    user_set = set()
    for i in range(0,num_users):
        user_set.add(user('user'+str(i+1)))
    series_set = set()
    for i in range(0,num_series):
        series_ = series('series'+str(i+1))
        for j in range(0,num_episodes):            
            series_.add_episode(episode("episode"+str(j+1)))
        series_set.add(series_)
    for _series in series_set:
        for _user in user_set:
            if random.randint(0,3) >= 3: # to create a less dense "network", each series is only watched by every 4th user
                _user.add_series(_series)
                #_series.add_user(_user) # maybe skip
                _episode_list = _series.get_episode_list()
                _episode_list[random.randint(0,len(_episode_list)-1)].add_user(_user) # only name / id of user instead of object. we already rely on index dict for username -> user object
    #index = {u.get_name() : u for u in user_list}
    #return (user_list, series_list, index)
    return user_set


def get_series_set_from_users(users):
    # we start with a set rather than a list to avoid having to check for redundancy
    series_set = set()
    for _user in users:
        for _series in _user.get_series_set():
            series_set.add(_series)
    return series_set



# this is the fastest one yet
def find_spoilers(lunchmates):
    spoiler_set = set()
    series_set = get_series_set_from_users(lunchmates)
    lunchmates_set = set(lunchmates)
    for _series in series_set:
        # find first (latest) episode with someone from the lunchmates-list
        offset = 0
        user_diffset = set()
        spoilers = set()
        _episode_list = _series.get_episode_list()
        _episode_list.reverse()
        print("checking episode list for users from lunchmates")
        for _episode in _episode_list:
            print(_episode.get_name())
            offset = offset + 1 # keep in mind where we found the first users from lunchmates so we can later check the remainder of the episodes
            _episode_user_set = _episode.get_user_set()
            user_diffset = lunchmates_set.intersection(_episode_user_set)
            if len(user_diffset) > 0:
                #print(user_diffset)
                spoilers = user_diffset
                break
        # check if earlier episodes contain users from the lunchmates-list
        print("searching for other users in episode list")
        for _episode in _episode_list[offset:]:
            print(_episode.get_name())
            _episode_user_set = _episode.get_user_set()
            user_diffset = lunchmates_set.intersection(_episode_user_set)
            # if yes, add the users from latest episode which are also in lunchmates-list to the spoiler list
            if len(user_diffset) > 0:
                for _spoiler in spoilers:
                    spoiler_set.add(_spoiler)
                break
    return spoiler_set


def find_lunchmates(user_instance, series):
    for _episode in series.get_episode_list():
        episode_users = _episode.get_user_list()
        if user_instance in episode_users:
            return episode_users
    return []

