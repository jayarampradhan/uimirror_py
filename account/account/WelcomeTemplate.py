def getDefault():
    '''
        This will get the default settings for the page
    '''
    return WelcomeTemplate()

def getContactViewSettings(contacts, compltedsteps):
    '''
       This will get the settings for the template page
       when user comes from the account contact import.
    '''
    view = WelcomeTemplate();
    compltedlsts = compltedsteps.split();
    view.step_completed = compltedsteps;
    view.step2_class = 'progtrckr-ongoing'
    view.step2_status_class = ''
    view.data_from_ref = 'stp2';
    view.data_tab_ref = '_um_progtrckr_2';
    view.data_from_next_ref = 'stp3';
    view.data_tab_next_ref = '_um_progtrckr_3';
    view.data_from_prv_ref = '1';
    view.data_tab_prv_ref = '_um_progtrckr_1';
    view.data = contacts;
    view.datatype = 'contacts';
    
    if '1' in compltedlsts:
        view.step1_class = 'progtrckr-done'
        view.step1_status_class = 'hidden'
        
    else:
        view.step1_class = 'progtrckr-skip'
        view.step1_status_class = 'hidden'
            
    if '3' in compltedlsts:
        view.step3_class = 'progtrckr-done'
        view.step3_status_class = 'hidden'
    else:
        view.step3_class = 'progtrckr-todo'
        view.step3_status_class = 'hidden'
        
    return view;     

class WelcomeTemplate(object):
    
    #Step classes
    step1_class = 'progtrckr-ongoing'
    step2_class = 'progtrckr-todo'
    step3_class = 'progtrckr-todo'
    #Inavlid messages
    INVLDMSG = ''
    INVLDSUG = ''
    #Individual Steps Class
    step1_status_class = ''
    step2_status_class = 'hidden'
    step3_status_class = 'hidden'
    
    #Data Attribute Reference
    data_from_next_ref = 'stp2'
    data_from_ref = 'stp1'
    data_tab_ref = '_um_progtrckr_1'
    data_tab_next_ref = '_um_progtrckr_2'
    data_from_prv_ref = ''
    data_tab_prv_ref = ''
    #Completeted Track
    step_completed=''
    #responses
    data = ''
    datatype = ''
    
