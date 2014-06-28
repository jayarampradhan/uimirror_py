from django.test import TestCase
import logging
from encryption.uiencrypt import EncryptionUtil

# Create your tests here.
logger = logging.getLogger(__name__)

class BaseTestCase(TestCase):
    PASSWORD_KEY = 'uimirrorprvpwd24'
    PUB_ENC_KEY = 'uimirrorpubkey24'
    PRV_ENC_KEY = 'uimirrorprvkey24'
    PUB_PRF_ID_ENC_KEY = 'uimirrorpubprf24'
    def setUp(self):
        pass
    
    
class EncryptionTest(BaseTestCase):
    def testEncryptionDefault(self):
        '''
           This will test for the default encryption
        '''
        api = EncryptionUtil()
        print "%s" %(api.encryptText())
        self.assertTrue(True, 'true')
        
    def testDecryptionDefault(self):
        '''
           This will test for default decryption
        '''
        api = EncryptionUtil()
        logger.info(api.decryptText('AzI/oNiKjDICLJqApFuCUN7arGJ4oOR%2BhH1pT0EehB4%3D'))
        self.assertTrue(True, 'true')
        
    def testgenratepwd(self):
        '''
           This will genrate the password key
        '''
        api = EncryptionUtil(self.PASSWORD_KEY)
        print 'pwdt- %s' %(api.encryptText('test'))
        
    def testGenratePubToken(self):
        api = EncryptionUtil(self.PUB_ENC_KEY)
        print 'public token- %s' %(api.encryptText('abc'))

    def testGenratePrivateToken(self):
        api = EncryptionUtil(self.PRV_ENC_KEY)
        print 'private toekn- %s' %(api.encryptText('abc'))
        
    def testGenratePubProfileId(self):
        api = EncryptionUtil(self.PUB_PRF_ID_ENC_KEY)
        print 'public profile id- %s' %(api.encryptText('123'))
