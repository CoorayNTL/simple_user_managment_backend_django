from django.contrib.auth.tokens import PasswordResetTokenGenerator#we can get the verification token from here

from six import text_type   

class TokenGenerator(PasswordResetTokenGenerator): #TokenGenerator is a class that is inheriting from PasswordResetTokenGenerator
    def _make_hash_value(self, user, timestamp):
        return (
        text_type(user.pk) + text_type(timestamp) 
        # text_type(user.profile.signup_confirmation)
        ) #this is the token that we will send to the 
    


generate_token = TokenGenerator() #this is the object of the class TokenGenerator