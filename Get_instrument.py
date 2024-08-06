from CFX_client_Registration import open_client, close_client
import time

#from helper_functions import call_csharp_method
import clr
clr.AddReference("C:/BioRobot/PCR_station-main/PCR_API_code/Source/Example_Application/bin/Release/BioRad.Example_Client_Wrapper.dll")

from BioRad.Example_Client_Wrapper import CFXManagerClientWrapper
client_wrapper=CFXManagerClientWrapper()


def get_instrument_status(client_wrapper, max_retries=5, delay=2):
    for attempt in range(max_retries):
        try:
            status_list=CFXManagerClientWrapper.GetInstrumentStatus()
            

            if status_list is not None and len(status_list) > 0:
                print("\nInstrument Status Summary:")
                for status in status_list:
                    print(f"Instrument: {status.BaseSerialNumber}")
                    print(f"  Name: {status.BaseName}")
                    print(f"  Status: {status.Status}")
                    print(f"  Block Type: {status.BlockType}")
                    print(f"  Sample Temp: {status.SampleTemp}°C")
                    print(f"  Lid Temp: {status.LidTemp}°C")
                    print(f"  Time Remaining: {status.EstimatedTimeRemaining}")
                    print("---")
                return status_list
            else:
                print(f"No instruments found or unable to retrieve status. Attempt {attempt + 1} of {max_retries}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                
        except Exception as e:
            print(f"Error getting instrument status: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)


    print("Failed to get instrument status after all retries.")
    return None


if __name__ == "__main__":
    client_wrapper = open_client()
    if client_wrapper:
        try:
            print("Waiting for instrument detection...")
            time.sleep(5)  # Wait for 5 seconds to allow for instrument detection
            status = get_instrument_status(client_wrapper)
            if status is None:
                print("Failed to get instrument status.")
        finally:
            close_client(client_wrapper)
    else:
        print("Failed to open client. Cannot proceed with getting instrument status.")

             

   
   

    
    
    


   
   

