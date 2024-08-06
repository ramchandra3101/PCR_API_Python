import clr
#import sys
import os
#from System import Configuration
from System.Configuration import ConfigurationManager
from CFX_manager_utilities import start_CFX_manager

def setup_configuration():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    config_name = f"{script_name}.exe.config"
    config_path = os.path.join(script_dir, config_name)
    if not os.path.exists(config_path):
        return False
    
    try:
        # Loading the configuration(Opening specific Client Configuration file)
        config = ConfigurationManager.OpenExeConfiguration(config_path)
        # Setting the configuration file path
        clr.System.AppDomain.CurrentDomain.SetData("APP_CONFIG_FILE", config_path)
        return True
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return False

# Add references and import
#clr.AddReference("D:/PCR_Station/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client.dll")
#clr.AddReference("D:/PCR_Station/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client_Wrapper.dll")
clr.AddReference("C:/BioRobot/PCR_station-main/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client.dll")
clr.AddReference("C:/BioRobot/PCR_station-main/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client_Wrapper.dll")
from BioRad.Example_Client import CFXManagerClient
from BioRad.Example_Client_Wrapper import CFXManagerClientWrapper

def create_client():
    try:
        start_CFX_manager()
        if not setup_configuration():
            print("Failed to set up configuration.")
            return False
        
        print("Attempting to create client...")
        result = CFXManagerClient.CreateClient()
        print(f"Client creation result: {result}")
        return result
    
    except Exception as e:
        print(f"Error creating client: {str(e)}")
        return False
    

def abort_client():
    try:
        CFXManagerClient.AbortClient()
        print("Client aborted successfully.")
    except Exception as e:
        print(f"Error aborting client: {str(e)}")


def is_connected():
    try:
        create_client()
        result = CFXManagerClient.IsConnected()
        print(f"Client connected: {result}")
        return result
    except Exception as e:
        print(f"Error checking connection: {str(e)}")
        return False
    
def SendRequest(request: str):
    try:
        if not is_connected():
            print("Client not connected")
            return None
        client=CFXManagerClient()
        response = client.SendServiceRequest(request)
        print(f"Response: {response}")
        return response
    except Exception as e:
        print(f"Error sending request: {str(e)}")
        return None
    
    
        




    
   
    
    





   



   
    
    