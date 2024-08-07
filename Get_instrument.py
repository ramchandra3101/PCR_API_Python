from CFX_client_Registration import open_client, close_client
import time

def get_instrument_status(client_wrapper, max_retries=5, delay=2):
    for attempt in range(max_retries):
        try:
           

            status_list=client_wrapper.GetInstrumentStatus()
                

            if status_list is not None and len(status_list) > 0:
                print("\nInstrument Status Summary:")
                for status in status_list:
                    serial_number= status.BaseSerialNumber
                    print(f"Instrument: {status.BaseSerialNumber}")
                    print(f"  Name: {status.BaseName}")
                    print(f"  Status: {status.Status}")
                    print(f"  Block Type: {status.BlockType}")
                    print(f"  Sample Temp: {status.SampleTemp}°C")
                    print(f"  Lid Temp: {status.LidTemp}°C")
                    print(f"  Time Remaining: {status.EstimatedTimeRemaining}")
                    print("---")
                return serial_number
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

def open_lid(client_wrapper, serial_number):
    try:
        if client_wrapper:
            if client_wrapper.OpenLid(serial_number):
                print("Lid opened successfully.")
                return True
            else:
                print("Failed to open lid.")
                return False
    except Exception as e:
        print(f"Error opening lid: {str(e)}")
        return False
    
def close_lid(client_wrapper, serial_number):
    try:
        if client_wrapper:
            if client_wrapper.CloseLid(serial_number):
                print("Lid closed successfully.")
                return True
            else:
                print("Failed to close lid.")
                return False
    except Exception as e:
        print(f"Error closing lid: {str(e)}")
        return False


if __name__ == "__main__":
    client_wrapper = open_client()
    if client_wrapper:
        try:
            print("Waiting for instrument detection...")
            time.sleep(5)  # Wait for 5 seconds to allow for instrument detection
            serial_number = get_instrument_status(client_wrapper)
            if serial_number is None:
                print("Failed to get instrument status.")
            else:
                print(f"Successfully retrieved status for instrument {serial_number}")
                print("Do you want to open the lid?")
                response = input("Enter 'Y' to open the lid or any other key to exit: ")
                if response.lower() == "y":
                    open_lid(client_wrapper, serial_number)
                
                print("Do you want to close the lid?")
                response = input("Enter 'Y' to close the lid or any other key to exit: ")
                if response.lower() == "y":
                    close_lid(client_wrapper, serial_number)
                    

        finally:
            close_client(client_wrapper)
    else:
        print("Failed to open client. Cannot proceed with getting instrument status.")

             

   
   

    
    
    


   
   

