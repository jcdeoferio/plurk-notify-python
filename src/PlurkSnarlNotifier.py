#requires simplejson, PySnarl
import PySnarl, simplejson, urllib2, urllib, time, ConfigParser
from time import localtime, strftime, gmtime
class PlurkSnarlNotifier(object):
    api_key = 'UqHifByhsRxXpHtgP102o22Jvy7yHZZ0'
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        self.encode = urllib.urlencode
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
        message = ''
        try:
            fp = self.opener.open(self.get_api_url('/Users/login'),
                                  self.encode({'username': self.username,
                                               'password': self.password,
                                               'api_key': self.api_key}))
        except:
#            result = simplejson.load(fp)
#            self.snarlShowMessage('Plurk', result['error_text'])
            return
        prevTime = gmtime()
        firstTime = False
        while True:
            currTime = gmtime()
            fp = self.opener.open(self.get_api_url('/Timeline/getPlurks'),
                                  self.encode({'limit': 5,
                                               'api_key': self.api_key}))
            result = simplejson.load(fp)
            if 'error_text' in result:
                self.snarlShowMessage('Plurk', result['error_text'])
            else:
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
                    if firstTime == False:
                        self.snarlShowMessage('Plurk', message, image)
                    elif posted > prevTime:
                        self.snarlShowMessage('Plurk', message, image)
                firstTime = True
                prevTime = currTime
                time.sleep(15)
                
config = ConfigParser.RawConfigParser()
config.read('settings.ini')
username = config.get('login','username')
password = config.get('login','password')           
test = PlurkSnarlNotifier(username,password)
test.run()
