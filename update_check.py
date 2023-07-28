## Github Update Checker
import TouchPortalAPI
import requests
import base64
from TPPEntry import PLUGIN_ID

#PLUGIN_NAME = "TikTokLive"
GITHUB_USER_NAME = "GitagoGaming"
GITHUB_PLUGIN_NAME = "TikTok-Live-Events--TouchPortal"



def plugin_update_check(plugin_version:str):
    """ Checks Github for the latest version of the plugin
    - Returns patchnotes on notification if there is a new version 
    """
    try:
        github_check = TouchPortalAPI.Tools.updateCheck(GITHUB_USER_NAME, GITHUB_PLUGIN_NAME)
      
        if github_check.replace('v','').replace(".","") > plugin_version:
            ### Pulling Patch Notes for Notification
            try:
                r = requests.get(f"https://api.github.com/repos/{GITHUB_USER_NAME}/{GITHUB_PLUGIN_NAME}/contents/recent_patchnotes.txt") 
                if r.status_code == 404:
                    print("No Patch Notes Found")
                    message = ""
                else:
                    base64_bytes = r.json()['content'].encode('ascii')
                    message_bytes = base64.b64decode(base64_bytes)
                    message = message_bytes.decode('ascii')
            except Exception as e:
                message = ""
                print("Error Plugin Update Check: ", e)
            return github_check, message
        else:
            return False, False
        
    except Exception as e:
        print("Something went wrong checking update", e)
        
        
        
        