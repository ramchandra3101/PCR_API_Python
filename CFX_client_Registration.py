
import clr
from CFX_client import is_connected
from CFX_manager_utilities import stop_CFX_manager
#clr.AddReference("D:/PCR_Station/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client_Wrapper.dll")

clr.AddReference("C:/BioRobot/PCR_station-main/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client_Wrapper.dll")
from BioRad.Example_Client_Wrapper import CFXManagerClientWrapper


def open_client():
    try:
        # Create an instance of CFXManagerClientWrapper
        client_wrapper = CFXManagerClientWrapper()
        
        if is_connected():
            if client_wrapper.OpenClient():
                print("Client opened successfully.")
                #for message in client_wrapper.LogMessages:
                    #print(f"C# Log:{message}")
                return True
            else:
                print("Failed to open client.")
                #for message in client_wrapper.LogMessages:
                    #print(f"C# Log: {message}")
                return False
        else:
            print("Client is not connected.")
            return False
    except Exception as e:
        print(f"Error opening client: {str(e)}")
        return False
    

def close_client(client_wrapper):
    if client_wrapper is not None:
        try:
            client_wrapper.CloseClient()
            #for message in client_wrapper.LogMessages:
                    #print(f"C# Log: {message}")
            print(f"C# Log: {message}")
            stop_CFX_manager()
            print("Client closed successfully.")
            
            return True
        except Exception as e:
            print(f"Error closing client: {str(e)}")
            
            return False
        
    else:
        print("No active client to close.")
        stop_CFX_manager()
        return False
    
