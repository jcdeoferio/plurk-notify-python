#requires simplejson, PySnarl
import PySnarl, simplejson, urllib2, urllib, time
from time import localtime, strftime, gmtime
class PlurkSnarlNotifier(object):
    api_key = 'UqHifByhsRxXpHtgP102o22Jvy7yHZZ0'
    def __init__(self, username, password):
        self.username = username
        self.password = password
        if PySnarl.snGetVersion() != False:
            (major, minor) = PySnarl.snGetVersion()
            print ('Found Snarl version', str(major) + "." + str(minor), 'running.')    
        else:
            print ("Sorry Snarl does not appear to be running")
            
    def get_api_url(self, str):
        return 'http://www.plurk.com/API%s' % str
    
    def snarlShowMessage(self, title, msg, image=''):
        id = PySnarl.snShowMessage(title, msg, timeout=15, iconPath=image)
        
    def run(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        encode = urllib.urlencode
        fp = opener.open(self.get_api_url('/Users/login'),
                         encode({'username': self.username,
                                 'password': self.password,
                                 'api_key': self.api_key}))
        prevTime = gmtime()
        while True:
            currTime = gmtime()
            fp = opener.open(self.get_api_url('/Timeline/getPlurks'),
                             encode({'limit': 5,
                                     'offset': strftime("%Y-%m-%dT%H:%M:%S", currTime),
                                     'api_key': self.api_key}))
            result = simplejson.load(fp)
            for plurk in result['plurks']:
                user = result['plurk_users'][str(plurk['owner_id'])]
                if 'display_name' in result['plurk_users'][str(plurk['owner_id'])]:
                    name = user['display_name']
                else:
                    name = user['nick_name']
                    
                if 'qualifier_translated' in plurk:
                    qualifier = plurk['qualifier_translated']
                else:
                    qualifier = plurk['qualifier']
                    
                if user['has_profile_image'] == 1 and user['avatar'] == 'null':
                    image = 'http://avatars.plurk.com/' + str(user['id']) + '-big.jpg'
                elif user['has_profile_image'] == 1 and user['avatar'] != 'null':
                    image = 'http://avatars.plurk.com/' + str(user['id']) + '-big' + str(user['avatar']) + '.jpg'
                if user['has_profile_image'] == 0:
                    image = 'http://www.plurk.com/static/default_big.gif'
                 
                posted = time.strptime(plurk['posted'], '%a, %d %b %Y %H:%M:%S GMT')
                message = name + ' ' + qualifier + ' ' + plurk['content_raw']
                print posted
                print prevTime
                if posted > prevTime:
                    self.snarlShowMessage('Plurk', message, image)
            time.sleep(10)
            prevTime = currTime
            
            
test = PlurkSnarlNotifier('username', 'password')
test.run()
