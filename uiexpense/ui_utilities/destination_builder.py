from django.conf import settings


UIMIRROR_DEST = getattr(settings, "UIM_HOME_URL", 'https://uimirror.com');
UIMIRROR_EXP_DEST = getattr(settings, "UIM_EXPENSE_HOME_URL", 'https://expense.uimirror.com');
UIMIRROR_CHAL_DEST = getattr(settings, "UIM_CHAL_HOME_URL", 'https://challenge.uimirror.com');
UIMIRROR_CAL_DEST = getattr(settings, "UIM_CAL_HOME_URL", 'https://callendar.uimirror.com');
def getDestinationByAppCode(app_code):
    '''
        This will determine destination based on app code.
        @param app_code: Application code, where request came from.
    '''
    if app_code == "1":
        destination = UIMIRROR_DEST;
    elif app_code == "2":
        destination = UIMIRROR_EXP_DEST;
    elif app_code == "3":
        destination = UIMIRROR_CAL_DEST;
    elif app_code == "4":
        destination = UIMIRROR_CHAL_DEST;
    else:
        destination = UIMIRROR_DEST;
            
    return destination;
    