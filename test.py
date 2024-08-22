import tkinter as tk
from tkinter import messagebox
import tkinter.messagebox
import customtkinter
import time
import threading
import sys  # Import the sys module
import u6 
    

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self, master=None):
        super().__init__()
        
        # to remove the header enable it 
        #self.overrideredirect(True)
        
        self.create_widgets()
        
        

    # Connect to the LabJack U6-Pro
        #self.d = u6.U6()
        try:
            self.d = u6.U6()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to the LabJack: {str(e)}")
            sys.exit()

    # Define the digital output lines for solonides adn switch 
        self.solonid_high_pressure = 9  # switch 1
        #self.solonid_low_pressure = 11   # switch 2
        self.solonid_vent =  8          # switch 0
        self.door_switch =  2            #switch 3


        ## Turn off all the switches when the program starts 
        self.d.setDOState(self.solonid_vent, 0)        
        self.d.setDOState(self.solonid_high_pressure, 0)
        #self.d.setDOState(self.solonid_low_pressure, 0)
        self.d.setDOState(10, 0)

     # configure window
        self.title("High Pressure Test")
        self.geometry(f"{1025}x{568}") 
        
    # Start the door status thread
        self.start_door_status_thread()


    def start_door_status_thread(self):
        self.door_status_thread = threading.Thread(target=self.run_door_status)
        self.door_status_thread.daemon = True  # Set the thread as a daemon so it exits when the main program ends
        self.door_status_thread.start() 

    def run_door_status(self):
        prev_door_status = None

        while True:
            door_status = self.get_door_status()

            if door_status != prev_door_status:
                self.update_door_status(door_status)
                prev_door_status = door_status
            time.sleep(1)

    def get_door_status(self):
        door = self.d.getFeedback(u6.BitStateRead(5))## FIO pin 2
        door_value = door[0]  # Assuming the door status is stored at index 0 of the list
        door_integer = int(door_value)
        return 1 - door_integer ## this control the logic of the door

    def update_door_status(self, door_status):
        message = "Door is Open. Please close it.\n" if door_status == 0 else "Door is Closed. Start the test.\n" 
        self.message_textbox.insert(tk.END, message)
        self.opendoorbutton.configure(fg_color="red", text="Close Door") if door_status == 0 else self.opendoorbutton.configure(fg_color="green", text="Open Door")
        self.door_indicator.configure(fg_color="red") if door_status == 0 else self.door_indicator.configure(fg_color="green")


    ###

    ## Emergency part of the code
        
        # Start the emergency status thread
        self.start_emergency_status_thread()

    

    def start_emergency_status_thread(self):
        self.emergency_status_thread = threading.Thread(target=self.run_emergency_status)
        self.emergency_status_thread.daemon = True  # Set the thread as a daemon so it exits when the main program ends
        self.emergency_status_thread.start() 

    def run_emergency_status(self):
        prev_emergency_status = None

        while True:
            emergency_status = self.get_emergency_status()

            if emergency_status != prev_emergency_status:
                self.update_emergency_status(emergency_status)
                prev_emergency_status = emergency_status
            time.sleep(1)

    def get_emergency_status(self):
        emergency = self.d.getFeedback(u6.BitStateRead(4))## FIO pin 3
        emergency_value = emergency[0]  # Assuming the door status is stored at index 0 of the list
        emergency_integer = int(emergency_value)
        return 1 - emergency_integer ## this control the logic of for emergency

    def update_emergency_status(self, emergency_status):
        message = "Emergency!!" if emergency_status == 0 else "" 
        self.message_textbox.insert(tk.END, message)
        self.emergency_indicator.configure(fg_color="red") if emergency_status == 0 else self.emergency_indicator.configure(fg_color="green")
    ###
        


    ## Widgets for the app
    def create_widgets(self):

        
        self.frame_1 = customtkinter.CTkFrame(self)
        self.frame_1.pack(pady=10, padx=10, fill="both", expand=True)

        self.startbutton = customtkinter.CTkButton(self.frame_1, width=150, height=70, command=self.startbutton_callback, text="Start Test", fg_color="green", border_width=2)
        self.startbutton.place(x=10, y=20)

        self.stopbutton = customtkinter.CTkButton(self.frame_1, width=150, height=70, command=self.stop, text="Stop Test", fg_color="red",border_width=2)
        self.stopbutton.place(x=200, y=20)

        self.message_lebel = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Message",font=("Arial", 13))
        self.message_lebel.place(x=470, y=85)
        
        self.message_textbox = customtkinter.CTkTextbox(self.frame_1, width=300, height=250,font=("Arial", 13))
        self.message_textbox.place(x=470, y=110)

        self.pressure_sensor_regulator = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Pressure Sensor Regulator", font=("Arial", 14))
        self.pressure_sensor_regulator.place(x=430, y=40)

        self.pressure_sensor_regulator_tabview = customtkinter.CTkTextbox(self.frame_1, width=150, height=35,font=("Arial", 15))
        self.pressure_sensor_regulator_tabview.place(x=620, y=40)

        self.pressure_sensor1 = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Pressure Sensor 1",font=("Arial", 13))
        self.pressure_sensor1.place(x=10, y=120)

        self.pressure_sensor1_tabview = customtkinter.CTkTextbox(self.frame_1, width=150, height=35,font=("Arial", 15))
        self.pressure_sensor1_tabview.place(x=130, y=120)

        self.pressure_sensor2 = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Pressure Sensor 2",font=("Arial", 13))
        self.pressure_sensor2.place(x=10, y=200)

        self.pressure_sensor2_tabview = customtkinter.CTkTextbox(self.frame_1, width=150, height=35,font=("Arial", 15))
        self.pressure_sensor2_tabview.place(x=130, y=200)

        self.pressure_sensor3 = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Pressure Sensor 3",font=("Arial", 13))
        self.pressure_sensor3.place(x=10, y=280)

        self.pressure_sensor3_tabview = customtkinter.CTkTextbox(self.frame_1, width=150, height=35,font=("Arial", 15))
        self.pressure_sensor3_tabview.place(x=130, y=280)

        self.test1_indicator = customtkinter.CTkFrame(self.frame_1, fg_color="grey", width=100, height=50)
        self.test1_indicator.place(x=10, y=350)

        self.test1_label = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Test", font=("Arial", 15))
        self.test1_label.place(x=35, y=400)

        #self.test2_indicator = customtkinter.CTkFrame(self.frame_1, fg_color="grey", width=100, height=50)
        #self.test2_indicator.place(x=170, y=350)

        #self.test2_label = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Test 2", font=("Arial", 15))
        #self.test2_label.place(x=195, y=400)

        self.progressbar_label = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Test Progress", font=("Arial", 18))
        self.progressbar_label.place(x=10, y=450)

        self.progressbar = customtkinter.CTkProgressBar(self.frame_1, width=250, height=15)
        self.progressbar.place(x=10, y=500)

        self.door_label = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Door", font=("Arial", 15))
        self.door_label.place(x=770, y=520)
        
        self.door_indicator = customtkinter.CTkFrame(self.frame_1, fg_color="grey", width=100, height=50)
        self.door_indicator.place(x=740, y=470)

        self.sol_1_label = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Sol 1", font=("Arial", 15))
        self.sol_1_label.place(x=480, y=430)      

        self.fill_sol_1= customtkinter.CTkFrame(self.frame_1,fg_color="white", width=50, height=50)
        self.fill_sol_1.place(x=470, y=380)

        #self.sol_2_label = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="SOl 2", font=("Arial", 15))
        #self.sol_2_label.place(x=580, y=430)

        #self.fill_sol_2 = customtkinter.CTkFrame(self.frame_1,fg_color="white", width=50, height=50)
        #self.fill_sol_2.place(x=570, y=380)

        self.vent_label = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Vent", font=("Arial", 15))
        self.vent_label.place(x=580, y=430)

        self.vent= customtkinter.CTkFrame(self.frame_1,fg_color="white", width=50, height=50)
        self.vent.place(x=570, y=380)

        self.opendoorbutton = customtkinter.CTkButton(self.frame_1, width=150, height=70, command=self.door_callback, border_width=2)
        self.opendoorbutton.place(x=450, y=470)


        self.emergency_label = customtkinter.CTkLabel(self.frame_1, justify=customtkinter.LEFT, text="Emergency", font=("Arial", 15))
        self.emergency_label.place(x=880, y=520)
        
        self.emergency_indicator = customtkinter.CTkFrame(self.frame_1, fg_color="grey", width=100, height=50)
        self.emergency_indicator.place(x=870, y=470)    
 


    
   

    def door_callback(self):
        door_status = self.get_door_status()  # Invoke the method to get the door status
        if door_status == 1:
            self.d.setDOState(self.door_switch, 0)  # Turn on solenoid 1
            time.sleep(3)
        elif door_status == 0:
            self.d.setDOState(self.door_switch, 1)  # Turn on solenoid 1
            time.sleep(3)
        

    def slider_callback(self, value):
        self.progressbar.set(value)
    
    
    def measure_initial_pressure(self):
        # Define the calibration parameters for your specific pressure sensor
        voltage_min = 0  # Minimum voltage from the pressure sensor in volts
        voltage_max = 5  # Maximum voltage from the pressure sensor in volts
        pressure_min = 0.0# Minimum pressure in mbar
        pressure_max = 1034.21  # Maximum pressure in mbar
        voltage_offset = 0.1  # Offset voltage from the pressure sensor in volts
        
        
        #initial presure
        ain0_voltage = self.d.getAIN(2)
        self.initial_pressure = (ain0_voltage - voltage_min) * (pressure_max - pressure_min) / (voltage_max - voltage_min) + pressure_min
        
    
    
    
    def pressurereading_small(self,sensor):   
        # Define the calibration parameters for your specific pressure sensor
        voltage_min = 0  # Minimum voltage from the pressure sensor in volts
        voltage_max = 5  # Maximum voltage from the pressure sensor in volts
        pressure_min = 0.0# Minimum pressure in mbar
        pressure_max = 1034.21  # Maximum pressure in mbar
        voltage_offset = 0.1  # Offset voltage from the pressure sensor in volts
        
        
        # Continuously read and display the pressure
        while not self.stopped:
            # Read the voltage from analog input channel 0
            ain0_voltage = self.d.getAIN(sensor)

            # Subtract the offset voltage
            #ain0_voltage -= voltage_offset

            # Calculate the pressure using a linear calibration
            pressure = (ain0_voltage - voltage_min) * (pressure_max - pressure_min) / (voltage_max - voltage_min) + pressure_min
            
                
            # normalzed pressure
            normalized_pressure = pressure - self.initial_pressure 
       
            # Print the pressure in psi
            return normalized_pressure

            # Delay for 1 second
            time.sleep(0.5)


    def pressurereading_big(self,sensor):   
        # Define the calibration parameters for your specific pressure sensor
        voltage_min = 0 #0.6115  # Minimum voltage from the pressure sensor in volts
        voltage_max = 5  # Maximum voltage from the pressure sensor in volts
        pressure_min = -12.0  # Minimum pressure in psi
        pressure_max = 7500  # Maximum pressure in psi
        voltage_offset = 0.111  # Offset voltage from the pressure sensor in volts

        # Continuously read and display the pressure
        while not self.stopped:
            # Read the voltage from analog input channel 0
            ain0_voltage = self.d.getAIN(sensor)

            # Subtract the offset voltage
            #ain0_voltage -= voltage_offset

            # Calculate the pressure using a linear calibration
            pressure = (ain0_voltage - voltage_min) * (pressure_max - pressure_min) / (voltage_max - voltage_min) + pressure_min

            # Print the pressure in psi
            return pressure

            # Delay for 1 second
            time.sleep(0.5)
 

    
    def run_pressure_monitoring(self):


            
        #test_failed = False  # Flag to track if the test has already failed

        test_failed_sensor1 = False  # Flag to track if the test has already failed for sensor 1
        test_failed_sensor2 = False  # Flag to track if the test has already failed for sensor 2
        test_failed_sensor3 = False  # Flag to track if the test has already failed for sensor 3

        while not self.stopped:

            #####Sensor 1 for unit 1

            
            # Check pressure sensor values
            sensor_1 = self.pressurereading_small(2)
            # Delete the previous content of the message_textbox
            self.pressure_sensor1_tabview.delete(1.0, tkinter.END)
            # Insert the updated sensor_1 value into message_textbox
            self.pressure_sensor1_tabview.insert(tkinter.END, "{:.1f} mbar".format(sensor_1))


            # Check if the pressure sensor fails the test
            if sensor_1 > 50:
                # Check if the test has already failed
                if not test_failed_sensor1:
                    test_failed_sensor1 = True
                    self.pressure_sensor1_tabview.configure(fg_color="red")  # Set background color to red
                    self.message_textbox.insert(tkinter.END, "Pressure Sensor 1 has failed the test.\n")
            else:
                test_failed_sensor1 = False
                self.pressure_sensor1_tabview.configure(fg_color="green")
            

            #####Sensor 2 for unit 2

                
            # Check pressure sensor values
            sensor_2 = self.pressurereading_small(2)
            # Delete the previous content of the message_textbox
            self.pressure_sensor2_tabview.delete(1.0, tkinter.END)
            # Insert the updated sensor_1 value into message_textbox
            self.pressure_sensor2_tabview.insert(tkinter.END, "{:.1f} mbar".format(sensor_1))

            # Check if the pressure sensor fails the test
            if sensor_2 > 50:
                # Check if the test has already failed
                if not test_failed_sensor2:
                    test_failed_sensor2 = True
                    self.pressure_sensor2_tabview.configure(fg_color="red")  # Set background color to red
                    self.message_textbox.insert(tkinter.END, "Pressure Sensor 2 has failed the test.\n")
            else:
                test_failed_sensor2 = False
                self.pressure_sensor2_tabview.configure(fg_color="green")
            

            #####Sensor 3 for unit 3

                
            # Check pressure sensor values
            sensor_3 = self.pressurereading_small(2)
            # Delete the previous content of the message_textbox
            self.pressure_sensor3_tabview.delete(1.0, tkinter.END)
            # Insert the updated sensor_1 value into message_textbox
            self.pressure_sensor3_tabview.insert(tkinter.END, "{:.1f} mbar".format(sensor_1))

            # Check if the pressure sensor fails the test
            if sensor_3 > 50:
                # Check if the test has already failed
                if not test_failed_sensor3:
                    test_failed_sensor3 = True
                    self.pressure_sensor3_tabview.configure(fg_color="red")  # Set background color to red
                    self.message_textbox.insert(tkinter.END, "Pressure Sensor 3 has failed the test.\n")
            else:
                test_failed_sensor3 = False
                self.pressure_sensor3_tabview.configure(fg_color="green")

            

            sensor_regulator = self.pressurereading_big(3)
            self.pressure_sensor_regulator_tabview.delete(1.0, tkinter.END)
            self.pressure_sensor_regulator_tabview.insert(tkinter.END, "{:.1f} PSI".format(sensor_regulator))

            

            # Delay for 1 second between pressure readings
            time.sleep(0.5)


    def run_tests(self):

    
        progress = 0
        
        # Start the test
        for test1_iteration in range(3):
            # Check if the stop button is pressed
            if self.stopped:
                break

            # Check if the door is open
            if self.get_door_status() == 0 or self.get_emergency_status() == 0:
                self.stop()
                return

            
            # Test 1
            #self.fill_sol_2.configure(fg_color="red")

            self.d.setDOState(self.solonid_high_pressure, 1)  # Turn on solenoid 1
            self.fill_sol_1.configure(fg_color="green")
            time.sleep(20)
            
            self.d.setDOState(self.solonid_high_pressure, 0)  # Turn off solenoid 1
            self.fill_sol_1.configure(fg_color="red")
            time.sleep(0.5)
            
            self.d.setDOState(self.solonid_vent, 1)  # Turn on vent
            self.vent.configure(fg_color="green")
            time.sleep(3)
            
            self.d.setDOState(self.solonid_vent, 0)  # Turn off vent
            self.vent.configure(fg_color="red")
            
            ##progress bar
            progress+=(1/3)
            self.slider_callback(progress)

        if not self.stopped:
            # Complete Test 1
            self.test1_indicator.configure(fg_color="green")
            self.message_textbox.insert(tkinter.END, "Testing has Completed \n") ### new addition for signal pressure rating test



##        for test2_iteration in range(3):
##            # Test 2
##
##            # Check if the stop button is pressed
##            if self.stopped:
##                break
##
##            # Check if the door is open
##            if self.get_door_status() == 0 or self.get_emergency_status() == 0:
##                self.stop()
##                return
##            
##            self.fill_sol_1.configure(fg_color="red")
##
##            self.d.setDOState(self.solonid_low_pressure, 1)  # Turn on solenoid 2
##            self.d.setDOState(self.solonid_high_pressure, 1)
##            self.fill_sol_2.configure(fg_color="green")
##            time.sleep(2)
##            
##            self.d.setDOState(self.solonid_low_pressure, 0)  # Turn off solenoid 2
##            self.d.setDOState(self.solonid_high_pressure, 0)
##            self.fill_sol_2.configure(fg_color="red")
##            time.sleep(1)
##            
##            self.d.setDOState(self.solonid_vent, 1)  # Turn on vent
##            self.vent.configure(fg_color="green")
##            time.sleep(2)
##            
##            self.d.setDOState(self.solonid_vent, 0)  # Turn off vent
##            self.vent.configure(fg_color="red")
##
##            ##progress bar
##            progress+=(1/6)
##            self.slider_callback(progress)
##
##        if not self.stopped:
##            # Complete Test 2
##            self.test2_indicator.configure(fg_color="green")
##            self.message_textbox.insert(tkinter.END, "Testing has Completed \n")
            



    def stop(self):
        self.stopped = True
        self.message_textbox.insert(tkinter.END, "Test is stopping... \n")
        # Turn off all solenoids and indicators
        self.d.setDOState(self.solonid_high_pressure, 0)
        self.fill_sol_1.configure(fg_color="red")
        #self.d.setDOState(self.solonid_low_pressure, 0)
        #self.fill_sol_2.configure(fg_color="red")
        
        self.d.setDOState(self.solonid_vent, 1)
        self.vent.configure(fg_color="green")
        self.update()
        # Delay for 5 seconds
        time.sleep(5)
        

        self.d.setDOState(self.solonid_vent, 0)
        self.vent.configure(fg_color="red")
        self.update()

        # Reset all indicators and colors
        self.fill_sol_1.configure(fg_color="red")
        #self.fill_sol_2.configure(fg_color="red")
        self.vent.configure(fg_color="red")
        self.test1_indicator.configure(fg_color="grey")
        #self.test2_indicator.configure(fg_color="grey")

        self.message_textbox.insert(tkinter.END, "Testing has stopped \n")
        
        
          
    def startbutton_callback(self):
        door_status = self.get_door_status()  # Invoke the method to get the door status
        if door_status == 0:
            self.message_textbox.insert(tkinter.END,"The door is Open. Code execution halted. \n")
        else:
            self.stopped = False


        emergency_status = self.get_emergency_status()  # Invoke the method to get the door status
        if emergency_status == 0:
            self.message_textbox.insert(tkinter.END,"Emergency!!!. Code execution halted. \n")
        else:
            self.stopped = False


            self.measure_initial_pressure()
            self.slider_callback(0)
            
            # Reset all indicators and colors
            self.fill_sol_1.configure(fg_color="red")
            #self.fill_sol_2.configure(fg_color="red")
            self.vent.configure(fg_color="red")
            self.test1_indicator.configure(fg_color="grey")
            #self.test2_indicator.configure(fg_color="grey")


            # Reset all indicators and colors after stopping
            self.pressure_sensor1_tabview.configure(fg_color="grey")

            # Clear previous reports
            self.message_textbox.delete(1.0, tkinter.END)

            # Create thread objects for each function
            thread1 = threading.Thread(target = self.run_tests)
            thread2 = threading.Thread(target = self.run_pressure_monitoring)

            # Start both threads
            thread1.start()
            thread2.start()


    
if __name__ == "__main__":
    app = App()
    app.mainloop()
    



