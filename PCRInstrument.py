from CFX_client_Registration import open_client, close_client
import time
from typing import Optional, List, Tuple
import threading
import queue

# Constants
PROTOCOL_FILE = r"C:\Users\szhang\Desktop\PCR_API_Python\Protocol.prcl"
PLATE_FILE = r"C:\Users\szhang\Desktop\PCR_API_Python\Protocolandplatefiles\Shuo plate.pltd"
INSTRUMENT_DETECTION_WAIT = 5
LID_OPERATION_WAIT = 10
STATUS_UPDATE_INTERVAL = 5


class PCRInstrument:
    def __init__(self):
        self.client_wrapper = None
        self.serial_number = None
        self.status = None
        self.running = False
        self.status_queue = queue.Queue()

    def open_client(self) -> bool:
        self.client_wrapper = open_client()
        return self.client_wrapper is not None

    def close_client(self):
        if self.client_wrapper:
            close_client(self.client_wrapper)

    def get_instrument_status(self, max_retries: int = 5, delay: int = 2) -> Optional[Tuple[str, str]]:
        for attempt in range(max_retries):
            try:
                status_list = self.client_wrapper.GetInstrumentStatus()
                if status_list and len(status_list) > 0:
                    self._print_instrument_status(status_list)
                    self.serial_number = status_list[0].BaseSerialNumber
                    self.status = status_list[0].Status
                    return self.serial_number, self.status
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

    def _print_instrument_status(self, status_list: List):
        print("\nInstrument Status Summary:")
        for status in status_list:
            print(f"Instrument: {status.BaseSerialNumber}")
            print(f"  Name: {status.BaseName}")
            print(f"  Status: {status.Status}")
            print(f"  Block Type: {status.BlockType}")
            print(f"  Sample Temp: {status.SampleTemp}°C")
            print(f"  Lid Temp: {status.LidTemp}°C")
            print(f"  Time Remaining: {status.EstimatedTimeRemaining}")
            print(f"Current Step: {status.ProtocolStep}")
            print(f"Current Cycle: {status.RepeatStep}")
            print(f"Current Stage: {status.MototrizedLidPosition}")
            print("---")

    def _execute_action(self, action_name: str, action_function, *args) -> bool:
        try:
            if self.client_wrapper and action_function(*args):
                print(f"{action_name} successfully.")
                return True
            else:
                print(f"Failed to {action_name.lower()}.")
                return False
        except Exception as e:
            print(f"Error {action_name.lower()}: {str(e)}")
            return False

    def open_lid(self) -> bool:
        return self._execute_action("Lid opened", self.client_wrapper.OpenLid, self.serial_number)

    def close_lid(self) -> bool:
        return self._execute_action("Lid closed", self.client_wrapper.CloseLid, self.serial_number)

    def blink_led(self) -> bool:
        return self._execute_action("LED blinked", self.client_wrapper.Blink, self.serial_number)

    def start_run(self, run_params: dict) -> bool:
        success = self._execute_action("Run started", self.client_wrapper.RunProtocol,
                                       self.serial_number,
                                       run_params['protocol_file'],
                                       run_params['plate_File'],
                                       run_params['run_Note'],
                                       run_params['run_ID'],
                                       run_params['DataFileName'],
                                       run_params['LockInstrument'],
                                       run_params['Generate_report'],
                                       run_params['Report_Template'],
                                       run_params['ReportFileName'],
                                       run_params['mailID'])
        if success:
            self.running = True
            threading.Thread(target=self._update_status_thread, daemon=True).start()
        return success

    def stop_run(self) -> bool:
        success = self._execute_action("Run stopped", self.client_wrapper.StopRun, self.serial_number)
        if success:
            self.running = False
        return success

    def pause_run(self) -> bool:
        return self._execute_action("Run paused", self.client_wrapper.PauseRun, self.serial_number)

    def resume_run(self) -> bool:
        return self._execute_action("Run resumed", self.client_wrapper.ResumeRun, self.serial_number)
    
    def _update_status_thread(self):
        while self.running:
            status = self.get_instrument_status()
            if status:
                self.status_queue.put(status)
            time.sleep(STATUS_UPDATE_INTERVAL)

   

def get_user_input(prompt: str, valid_responses: List[str]) -> str:
    while True:
        response = input(prompt).lower()
        if response in valid_responses:
            return response
        print(f"Invalid input. Please enter one of {', '.join(valid_responses)}")

def print_status_updates(pcr: PCRInstrument):
    while pcr.running:
        try:
            status =pcr.status_queue.get(timeout=1)
            pcr._print_instrument_status(status)
        except queue.Empty:
            pass

def run_protocol(pcr: PCRInstrument, run_params: dict):
    if pcr.start_run(run_params):
        print("Run started. Monitoring status...")
        status_thread = threading.Thread(target=print_status_updates, args=(pcr,), daemon=True)
        status_thread.start()

        while pcr.running:
            action = get_user_input("Enter 's' to stop, 'p' to pause, 'r' to resume, or press Enter to continue: ", ['s', 'p', 'r', ''])
            if action == 's':
                pcr.stop_run()
                break
            elif action == 'p':
                pcr.pause_run()
            elif action == 'r':
                pcr.resume_run()

        status_thread.join()
        print("Run completed or stopped.")
    else:
        print("Failed to start the run.")

def main():
    pcr = PCRInstrument()

    if not pcr.open_client():
        print("Failed to open client. Cannot proceed with getting instrument status.")
        return

    try:
        print("Waiting for instrument detection...")
        time.sleep(INSTRUMENT_DETECTION_WAIT)

        status = pcr.get_instrument_status()
        if not status:
            print("Failed to get instrument status.")
            return

        print(f"Successfully retrieved status for instrument {pcr.serial_number}")
        print(f"Status: {pcr.status}")

        
        print("Be alert! The Lid is opening")
        pcr.open_lid()
        print(f"Status: {pcr.status}")

        time.sleep(LID_OPERATION_WAIT)

        print("Be alert! The Lid is closing")
        pcr.close_lid()
        time.sleep(LID_OPERATION_WAIT)
        print(f"Status: {pcr.status}")
        #pcr.blink_led()


        if get_user_input("Enter 'y' to start the run or any other key to exit: ", ['y']) != 'y':
            print("Exiting...")
            return

        run_params = {
            'protocol_file': PROTOCOL_FILE,
            'plate_File': PLATE_FILE,
            'run_Note': "This is a test run",
            'run_ID': "TestRun",
            'DataFileName': "",
            'LockInstrument': True,
            'Generate_report': True,
            'Report_Template': "",
            'ReportFileName': "",
            'mailID': "ramachandra.yerramsetti@uconn.edu"
        }

        run_protocol(pcr, run_params)
   
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        pcr.close_client()
    finally:
        pcr.close_client()


if __name__ == "__main__":
    main()