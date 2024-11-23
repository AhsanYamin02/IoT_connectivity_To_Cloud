import serial
import time

def send_at_command(command, port='/dev/ttyUSB0', baudrate=115200, timeout=1, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            # Open serial port
            with serial.Serial(port, baudrate, timeout=timeout) as ser:
                # Send AT command
                ser.write((command + '\r\n').encode())
                
                # Wait for response
                time.sleep(0.5)  # Adjust delay as needed
                response = ser.read(ser.in_waiting).decode().strip()
                
                # Print and log response
                print("Response:", response)
                log_response(command, response)
                
                # Check if the response is OK or not
                if 'OK' in response or response:
                    return response
            
        except serial.SerialException as e:
            print(f"Serial port error on attempt {attempt + 1}: {e}")
            attempt += 1
            time.sleep(1)  # Wait a bit before retrying
    print(f"Failed to send command after {retries} attempts: {command}")
    return None

def log_response(command, response, logfile='response_log.txt'):
    with open(logfile, 'a') as log:
        log.write(f"Command: {command}\nResponse: {response}\n\n")

def execute_block(commands, port='/dev/ttyUSB0', baudrate=115200, timeout=1, retries=3):
    for command in commands:
        response = send_at_command(command, port, baudrate, timeout, retries)
        if response is None:
            print(f"Block execution failed at command: {command}. Retrying the block...")
            return False
        time.sleep(5)  # 5 seconds gap between commands
    return True

# Block 1
block1 = [
    'AT+COPS?',
    'AT+CGDCONT=1,"IP","elisa","0.0.0.0",0,0',
    'AT^SICS=1,"dns1","0.0.0.0"',
    'AT^SICS=1,"dns2","0.0.0.0"',
    'AT+CGPADDR=1'
]

# Block 2
block2 = [
    'AT+CEREG?',
    'AT+CGREG?',
    'AT+CEREG=2',
    'AT+CGREG=2',
    'AT+CGATT=1'
]

# Block 3
block3 = [
    'AT+CESQ',
    'AT^SMONI'
]

# Block 4
block4 = [
    'AT^SICA=1,1',
    'AT^SISS=2,srvType,"Mqtt"',
    'AT^SISS=2,conId,"1"',
    'AT^SISS=2,address,"mqtt://193.167.189.184:1885;connackTimeout=30"',
    'AT^SISS=2,clientId,"351561110167505";',
    'AT^SISS=2,cleanSession,"1"',
    'AT^SISS=2,ipVer,"4"',
    'AT^SISS=2,cmd,"unsubscribe"',
    'AT^SISS=2,TopicFilter,"MQTTDemoListener"',
    'AT^SICA=1,2',
    'AT^SISO=2,2',
    'AT^SISD=2,"cleanParam"',
    'AT^SISU=2,"subscribe","MQTTDemoListener;2"'
]

# Block 5
block5 = [
    'AT^SISU=2,"publish","2;MQTTD;1;0;66"',
    'at^sisw=2,66'
]

def main():
    while not execute_block(block1):
        print("Retrying Block 1...")
    
    while not execute_block(block2):
        print("Retrying Block 2...")
    
    # Block 3 execution and response storage
    response_storage = []
    for command in block3:
        response = send_at_command(command, port='/dev/ttyUSB0', baudrate=115200)
        if response is None:
            print(f"Block 3 execution failed at command: {command}. Retrying the block...")
            response_storage = []
            break
        response_storage.append(response)
        time.sleep(5)
    else:
        # Calculate the total bytes of the stored responses
        total_bytes = sum(len(res) for res in response_storage)
        print(f"Total bytes from Block 3 responses: {total_bytes}")
    
    while not execute_block(block4):
        print("Retrying Block 4...")
    
    while not execute_block(block5):
        print("Retrying Block 5...")
    
    # Block 6 execution with stored value from Block 3
    if response_storage:
        stored_value = ''.join(response_storage)[:66]  # Take first 66 bytes
        send_at_command(f'SMONI: {stored_value}', port='/dev/ttyUSB0', baudrate=115200)

if __name__ == "__main__":
    main()
