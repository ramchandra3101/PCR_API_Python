from ctypes import *
import inspect
import clr
import time
# PCR_dll=cdll.LoadLibrary("D:/PCR_Station/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client_Wrapper.dll")
clr.AddReference("D:/PCR_Station/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client_Wrapper.dll")

from BioRad.Example_Client_Wrapper import CFXManagerUtilities

def start_CFX_manager():
    if CFXManagerUtilities.APICompatibleCFXManagerIsInstalled:
        print("CFX Manager is installed")

    else:
        print("CFX Manager is not installed")
    
    if CFXManagerUtilities.CFXManagerIsExecuting:
        print("CFX Manager is already running.")
    else:
        # Start CFX Manager in server mode
        if CFXManagerUtilities.StartCFXManagerAsServer():
            print("CFX Manager started successfully in server mode.")
        else:
            print("Failed to start CFX Manager in server mode.")
            return
        

def stop_CFX_manager():
        
    CFXManagerUtilities.StopCFXManager()
    print("CFX Manager stopped.")
        









