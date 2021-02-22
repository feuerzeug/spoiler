from multiprocessing import Process, Queue, Pool
import pickle
import random

   
class episode(object):
    def __init__(self, name=None, user_list=None):
        self._name = name
        self._user_list = []
    
    def get_name(self):
        return self._name
    
    def get_user_list(self):
        return self._user_list
    
    def add_user(self, user_instance):
        if type(user_instance) != user:
            raise TypeError("is not a user")
        self._user_list.append(user_instance)

    def delete_user(self, user_instance):
        _user_list.remove(user_instance)
        

class user(object): 
    def __init__(self, name, series_list=None):
        if series_list is None:
            self._series_list = []
        else:
            self._series_list = series_list
        self._name = name

    def __str__(self):
        return "<" + self._name + ", watching " + str(len(self._series_list)) + " series>"
    
    def get_series_list(self):
        return self._series_list
    
    def add_series(self, series_instance):
        if type(series_instance) != series:
            raise TypeError("is not a series")
        self._series_list.append(series_instance)

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
    return (user_set, series_set)

# just to test, whether it is the randomness that takes so long, here is a function which just adds all users to the first episode of each series
def build_test_set_norandom(num_users=3128, num_series=204, num_episodes=24):
    series_list = []
    for i in range(0,num_series):
        series_list.append(series('series'+str(i+1)))
        for j in range(0,num_episodes):
            series_list[i].add_episode(episode("episode"+str(j+1)))

    user_list = []
    for i in range(0,num_users):
        user_list.append(user('user'+str(i+1)))

    for _series in series_list:
        for _user in user_list:
            _user.add_series(_series)
            _series.add_user(_user)
            _episode_list = _series.get_episode_list()
            _episode_list[0].add_user(_user)
    return (user_list, series_list)



# this method is a little lazier and only looks at the top spoilers in each series, but still looks at every user at least once
# for 3128 users, 204 series with 24 episodes each this method needs 0.16 seconds, which is reasonable for a synchronous call to a web service
# for 30128 users, though, it takes ~ 14 seconds, which is too long
def spoiler_find_lazy(lunchmates):
    spoiler_list = []
    for _user in lunchmates:
        is_spoiler = False
        for _series in _user.get_series_list():
            if is_spoiler: # we need not consider this user again as a potential spoiler, because we already know he is one for this series
                break
            _episode_list = _series.get_episode_list()
            for i in range(len(_episode_list)):
                if _user in _episode_list[i].get_user_list():
                    _index = i
            if _index is None:
                raise AssertionError("inconsistent episode_list for "+_series.get_name()+". User "+_user.get_name()+" not in list but claims to watch series")
            for _episode in _episode_list[:_index]:
                for _spoilee in _episode.get_user_list():
                    if _spoilee in lunchmates:
                        is_spoiler = True # we need not consider this user again as a potential spoiler, because we already know he is one for this series
                        spoiler_list.append((_user.get_name(), _spoilee.get_name(), _series.get_name()))
                        break
    return spoiler_list


# this one is slower because of the use of a list instead of a set which needs a check for every insertion to avoid multiple entries in resulting list
def get_series_list_from_user_list(user_list):
    series_list = []
    for _user in user_list:
        for _series in _user.get_series_list():
            if _series not in series_list:
                series_list.append(_series)
    return series_list

def get_series_set_from_user_list_(user_list):
    # we start with a set rather than a list to avoid having to check for redundancy
    series_set = set()
    for _user in user_list:
        for _series in _user.get_series_list():
            series_set.add(_series)
    return series_set

def find_user_by_name(name, user_list):
    for _user in user_list:
        if _user.get_name() == name:
            return _user
    return None

# as it turns out, this runs for ages and should be handled differently
def find_user_list_by_names(names, user_list):
    user_list_result = set()
    for name in names:
        _user = find_user_by_name(name, user_list)
        if _user is not None:
            user_list_result.add(_user)
        else:
            raise AssertionError("can't find user with name \"%s\" in database", name)
    return list(user_list_result)


# helper function to test find_user-list_by_names()
def name_list(user_list_):
    name_list_ = []
    for user_ in user_list_:
        name_list_.append(user_.get_name())
    return name_list_


#def get_user_set_from_episode_list(episode_list, user_set):
#    users_found = set()
#    for _episode in episode_list:
#        _episode_user_set = set(_episode.get_user_list())
#        users_found.add(_episode_user_set)
#    return users_found

# this function is quite fast. I tried to only do the neccessary operations.
def find_spoilers(lunchmates):
    spoiler_list = []
    series_set = get_series_set_from_user_list_(lunchmates)
    lunchmates_set = set(lunchmates)
    for _series in series_set:
        # find first (latest) episode with someone from the lunchmates-list
        offset = 0
        user_diffset = set()
        spoilers = set()
        _episode_list = _series.get_episode_list()
        _episode_list.reverse()
        for _episode in _episode_list:
            offset = offset + 1 # keep in mind where we found the first users from lunchmates so we can later check the remainder of the episodes
            _episode_user_set = set(_episode.get_user_list())
            user_diffset = lunchmates_set.intersection(_episode_user_set)
            if len(user_diffset) > 0:
                #print(user_diffset)
                spoilers = user_diffset
                break
        # check if earlier episodes contain users from the lunchmates-list
        for _episode in _episode_list[offset:]:
            _episode_user_set = set(_episode.get_user_list())
            user_diffset = lunchmates_set.intersection(_episode_user_set)
            # if yes, add the users from latest episode which are also in lunchmates-list to the spoiler list
            if len(user_diffset) > 0:
                spoiler_list.append((spoilers, _series))
    return spoiler_list

# needs multiprocessing added
def find_spoilers_multiprocess(lunchmates, num_processes):
    queue = Queue()
    spoiler_list = []
    series_set = get_series_set_from_user_list_(lunchmates)
    lunchmates_set = set(lunchmates)
    series_list = list(series_set)
    pool = Pool(num_processes)
    limiter = int(len(series_list)/num_processes)
    args = []
    for i in range(num_processes-1):
        args.append((series_list[limiter*i:limiter*(i+1)],lunchmates_set))
    args.append((series_list[limiter*(num_processes-1):],lunchmates_set))
    result = pool.map(find_spoilers_in_series, args)
    return result

def find_spoilers_in_series(series_list, lunchmates_set):
    spoiler_list = []
    for _series in series_list:
    # find first (latest) episode with someone from the lunchmates-list
        offset = 0
        user_diffset = set()
        spoilers = set()
        _episode_list = _series.get_episode_list()
        _episode_list.reverse()
        for _episode in _episode_list:
            offset = offset + 1 # keep in mind where we found the first users from lunchmates so we can later check the remainder of the episodes
            _episode_user_set = set(_episode.get_user_list())
            user_diffset = lunchmates_set.intersection(_episode_user_set)
            if len(user_diffset) > 0:
                #print(user_diffset)
                spoilers = user_diffset
                break
        # check if earlier episodes contain users from the lunchmates-list
        for _episode in _episode_list[offset:]:
            _episode_user_set = set(_episode.get_user_list())
            user_diffset = lunchmates_set.intersection(_episode_user_set)
            # if yes, add the users from latest episode which are also in lunchmates-list to the spoiler list
            if len(user_diffset) > 0:
                spoiler_list.append((spoilers, _series))
    return spoiler_list

def find_lunchmates(user_instance, series):
    for _episode in series.get_episode_list():
        episode_users = _episode.get_user_list()
        if user_instance in episode_users:
            return episode_users
    return []

