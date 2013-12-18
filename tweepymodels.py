from google.appengine.ext import db

class Config(db.Model):
    """Model to store configuration.
    """
    value = db.StringProperty()
    updated_on = db.DateTimeProperty(auto_now=True)

    @staticmethod
    def get(name):
        config = Config.get_by_key_name(name)
        return config and config.value

    @staticmethod
    def set(name, value):
        Config(key_name=name,
               value=value
               ).put()


class Agent(db.Model):
    """Model to store user login data.
    """
    access_key = db.StringProperty()
    access_secret = db.StringProperty()

    @staticmethod
    def get(username):
        agent = Agent.get_by_key_name(username)
        return (agent.access_key, agent.access_secret)

    @staticmethod
    def set(username, access_key, access_secret):
        Agent(key_name=username,
              access_key=access_key,
              access_secret=access_secret).put()



class RequestToken(db.Model):
    """Model to store transitional request token when performing OAuth login.
    """

    value = db.StringProperty()

    @staticmethod
    def get(name):
        name = "%s" %name
        request_token = RequestToken.get_by_key_name(name)
        return request_token and request_token.value

    @staticmethod
    def set(name, value):
        name = "%s" %name
        RequestToken(key_name=name, value=value).put()
        
        
