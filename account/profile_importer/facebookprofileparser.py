import logging

from ui_utilities.dsutilities import DSUtility
from profile_importer.privacybuilder import PrivacyBuilder
from ui_utilities import month_mapper
from profile_importer import school_type_mapper


log = logging.getLogger(__name__)
class FaceBookProfileParser(object):
    '''
       This will utility class will be helpful to get the facebook profile in dictionary.
       
    '''
    ds_utility = DSUtility();
    privacy = PrivacyBuilder();
     
    def parseFbImport(self, profile, image):
        '''
           This will parse the FB import data, and transformed into UImirror record.
           @param profile: Imported Profile From faceBook.
           @param image: Imported profile Pic from Facebook.
        '''
        
        if not profile:
            return None;
        d = {}
        name = self.parseName(profile);
        if name:
            d = dict(d.items() + name.items());
        gender = self.parseGender(profile);
        if gender:
            d = dict(d.items() + gender.items());
        website = self.parseWebsite(profile);
        if website:
            d = dict(d.items() + website.items());
        dob = self.parseBirthDay(profile);
        if dob:
            d = dict(d.items() + dob.items());
        places = self.parseHomeTown(profile);
        if places:
            d = dict(d.items() + places.items());
        education = self.parseEducation(profile);
        if education:
            d = dict(d.items() + education.items());
        work = self.parseWork(profile);
        if work:
            d = dict(d.items() + work.items());
        singlevalue = self.parseSingleValue(profile, image);
        if singlevalue:
            d = dict(d.items() + singlevalue.items());
        aboutme = self.parseAboutMe(profile);
        if aboutme:
            d = dict(d.items() + aboutme.items());
        log.info(d);
        return d;
    
    def parseName(self, profile):
        '''
           This will get the name from facebook profile.
           @param profile: Profile details from Facebook.
        '''
        d = {}
        name = {}
        first_name = self.ds_utility.getlistitem(profile, 'first_name');
        if first_name:
            d['first'] = first_name;
        last_name = self.ds_utility.getlistitem(profile, 'last_name');
        if last_name:
            d['last'] = last_name;
        middle_name = self.ds_utility.getlistitem(profile, 'middle_name');
        if middle_name:
            d['middle'] = middle_name;
        
        if d:
            name['name'] = d;
            return name;
        else:
            return None;
        
    def parseGender(self, profile):
        '''
          This will parse the gender information of the user
        '''
        gender = self.ds_utility.getlistitem(profile, 'gender');
        if gender:
            d = {}
            d['gender'] = gender;
            return d;
        else:
            return None;
        
    def parseWebsite(self, profile):
        '''
           This will parse the web site information of the user.
        '''
        website_info = self.ds_utility.getlistitem(profile, 'website');
        if website_info:
            d = {}
            website = {}
            website['url'] = website_info;
            website['privacy'] = self.privacy.buildPrivacy("friends");
            d['website'] = website; 
            return d;
        else:
            return None;
        
    def parseBirthDay(self, profile):
        '''
           This will parse the birth day information of the user.
        '''
        
        date_of_birth = self.ds_utility.getlistitem(profile, 'birthday');
        if date_of_birth:
            day = {}
            year = {}
            dob = {}
            d = {}
            interims = date_of_birth.split("/");
            birth_date = month_mapper.monthDict[int(interims[0])]+" "+interims[1];
            day['day'] = birth_date;
            day['privacy'] =  self.privacy.buildPrivacy("friends");
            year['year'] = interims[2];
            year['privacy'] =  self.privacy.buildPrivacy("friends");#It should be only me
            dob['bday'] = day;
            dob['byear'] = year;
            d['dob'] = dob;
            return d;  
        else:
            return None;
    
    def parseHomeTown(self, profile):
        '''
           This will build the home town of the user if present
        '''
        home_town = self.ds_utility.getlistitem(profile, 'hometown');
        if home_town:
            home = self.privacy.buildPrivacy("friends");
            places = {}
            d = {}
            home['name'] = self.ds_utility.getlistitem(home_town, 'name');
            places['home'] = home;
            d['places'] = places; 
            return d;  
        else:
            return None;
        
    def parseEducation(self, profile):
        '''
           This will parse the education details of the user.
        '''
        education = self.ds_utility.getlistitem(profile, 'education');
        if education: 
            schools = []
            d = {}
            for school in education:
                school_dic = self.privacy.buildPrivacy("friends");
                duration = {}
                school_name = {}
                school_dtls = self.ds_utility.getlistitem(school, 'school');
                if school_dtls:
                    name = self.ds_utility.getlistitem(school_dtls, 'name');
                    school_name['name'] = name;
                    school_dic['school'] = school_name;
                school_type = self.ds_utility.getlistitem(school, 'type');
                if school_type:
                    school_dic['type'] = school_type_mapper.schoolTypeDict[school_type];
                
                year_dtls = self.ds_utility.getlistitem(school, 'year');
                if year_dtls:
                    #TODO work on end year
                    start_year = self.ds_utility.getlistitem(year_dtls, 'name');
                    duration['start'] = start_year;
                    #TODO end year check
                    duration['end'] = start_year;
                    school_dic['duration'] = duration;
                schools.append(school_dic);
            d['education'] = schools;
            return d;
        else:
            return None;
        
    def parseWork(self, profile):
        '''
           This will parse work details of the user
        '''
        works = self.ds_utility.getlistitem(profile, 'work');
        if works:
            job = []
            d = {}
            for work in works:
                job_dic = self.privacy.buildPrivacy("friends");
                company = {}
                location = {}
                employer_dtls = self.ds_utility.getlistitem(work, 'employer');
                if employer_dtls:
                    company_name = self.ds_utility.getlistitem(employer_dtls, 'name');
                    company['name'] = company_name;
                    job_dic['employer'] = company; 
                position_dtls = self.ds_utility.getlistitem(work, 'position');
                if position_dtls:
                    position = self.ds_utility.getlistitem(position_dtls, 'name');
                    job_dic['position'] = position;
                start_date = self.ds_utility.getlistitem(work, 'start_date');
                if start_date:
                    job_dic['start'] = start_date;
                end_date = self.ds_utility.getlistitem(work, 'end_date');
                if end_date:
                    job_dic['end'] = end_date;
                location_dtls = self.ds_utility.getlistitem(work, 'location');
                if location_dtls:
                    location_name = self.ds_utility.getlistitem(location_dtls, 'name');
                    location['name'] = location_name;
                    job_dic['location'] = location;
                job.append(job_dic) 
            d['work'] = job;
            return d;
        else:
            return None;
        
    def parseAboutMe(self, profile):
        '''
           This will parse the about me section.
        '''
        bio = self.ds_utility.getlistitem(profile, 'bio');
        if bio:
            d = {}
            about_me = self.privacy.buildPrivacy("friends");
            about_me['me'] = bio;
            d['bio'] = about_me;
            return d;
        else:
            return None;
        pass; 
         
    def parseSingleValue(self, profile, image):
        '''
           This will parse the single value facebook profile.
           @param profile: Profile details from Facebook.
           @param image: Profile Image of the user
        '''
        d = {}
        locale = self.ds_utility.getlistitem(profile, 'locale');
        if locale:
            d['locale'] = locale;
        timezone = self.ds_utility.getlistitem(profile, 'timezone');
        if timezone:
            d['tz'] = timezone;  
        if image:
            d['image'] = image;
            
        if d:
            return d;
        else:
            return None;
