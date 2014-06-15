
class PrivacyBuilder(object):
    '''
       This will help us to build the privacy for the user.
    '''
    def buildPrivacy(self, privacy_name, share_with = None, not_share_with = None):
        '''
           This will build the privacy.
           @param privacy_name: Which specifies name of the privacy like, public, friends, friends of friend, custom etc
           @param share_with: specifies if the privacy was custom then these value may present like profile id and name
           @param not_share_with: specifies if the privacy was custom then these value may present like profile id and name
        '''
        d = {}
        if not privacy_name:
            return None;
        else:
            d['privacy'] = privacy_name;
            
        custom = {}
        if share_with:
            custom['with'] = share_with;
        if not_share_with:
            custom['notwith'] = not_share_with;
            
        if custom:
            d['custom'] = custom; 
             
        return d;
    