import threading
import tkinter
import tkinter.messagebox
from time import sleep
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser

import serial
import serial.tools.list_ports

ports = ["Choose a port"]
ser = serial.Serial()


def choose_port():
    ser.port = chosen_port.get()
    try:
        ser.open()
        print(ser.portstr)
        tkinter.messagebox.showinfo("Port Set", "Port Set")
        sendMessageButton.configure(state=tkinter.NORMAL)
        startListeningButton.configure(state=tkinter.NORMAL)
    except Exception as e:
        tkinter.messagebox.showinfo("Port Not Set", str(e))
        exit()


def on_closing():
    if tkinter.messagebox.askokcancel("Quit", "Quit and close port?"):
        if ser.is_open:
            ser.close()
        f.close()
        top.destroy()


def send_message():
    if interval_entry1.get().isdigit() & interval_entry2.get().isdigit() & interval_entry3.get().isdigit() &\
            interval_entry4.get().isdigit():
        string_to_send = interval_entry1.get() + ":" + interval_entry2.get() + ":" + interval_entry3.get() + ":"\
                         + interval_entry4.get()
        ser.write(str.encode(string_to_send))
        print("message sent " + string_to_send)
    else:
        tkinter.messagebox.showinfo("Wrong Value", "Please input 4 numbers.")


def get_serial(ttid, stop):
    while True:
        if stop():
            break
        s = ser.readline()
        if s:
            db_line = str(datetime.now()) + ", " + s.decode("ASCII")
            print(db_line)  # Read the newest output from the Arduino
            f.write(db_line)
        sleep(.1)  # Delay for one tenth of a second
    f.close()
    print("stopped listening")


def stop_listening():
    global stop_listening_flag
    stop_listening_flag = True
    sendMessageButton.configure(state=tkinter.NORMAL)
    stopListeningButton.configure(state=tkinter.DISABLED)
    sendMessageButton.configure(state=tkinter.NORMAL)
    t.join()


def listen_to_arduino():
    # sendMessageButton.configure(state=tkinter.DISABLED)
    stopListeningButton.configure(state=tkinter.NORMAL)
    t.start()


def plot_sensor():
    plot_x = []
    plot_y = []
    with open('semaphore_schedule.csv') as file:
        for line in file:
                split_data = line.split(",")
                if "earthquake" in split_data[1]:
                    print(split_data)
                    plot_x.append(parser.parse(split_data[0]))
                    plot_y.append(int(split_data[2]))
    fig, ax = plt.subplots()
    ax.plot(plot_x, plot_y, 'b-')
    ax.xaxis_date()
    plt.show()


if __name__ == '__main__':
    stop_listening_flag = False
    f = open("semaphore_schedule.csv", "a+")

    top = tkinter.Tk()
    top.title("Arduino Semaphore Config Program")

    ser = serial.Serial()  # open first serial port
    print(ser.portstr)

    for n, (port_name, desc, hwid) in enumerate(sorted(serial.tools.list_ports.comports())):
        ports.append(port_name)

    chosen_port = tkinter.StringVar(top)
    if ports:
        chosen_port.set(ports[0])
    else:
        chosen_port.set("no ports available")
    portListWidget = tkinter.OptionMenu(top, chosen_port, *ports)
    portListWidget.pack()

    choosePortButton = tkinter.Button(top, text="Set Port", command=choose_port)
    choosePortButton.pack()

    interval_entry1 = tkinter.Entry(top)
    interval_entry2 = tkinter.Entry(top)
    interval_entry3 = tkinter.Entry(top)
    interval_entry4 = tkinter.Entry(top)

    interval_entry1.pack(padx=5, pady=10, side=tkinter.LEFT)
    interval_entry2.pack(padx=5, pady=10, side=tkinter.LEFT)
    interval_entry3.pack(padx=5, pady=10, side=tkinter.LEFT)
    interval_entry4.pack(padx=5, pady=10, side=tkinter.LEFT)

    sendMessageButton = tkinter.Button(top, text="Send Message", command=send_message)
    # sendMessageButton.configure(state=tkinter.DISABLED)
    sendMessageButton.pack(padx=5, pady=10)

    tid = 0
    t = threading.Thread(target=get_serial, args=(id, lambda: stop_listening_flag))
    t.daemon = True

    startListeningButton = tkinter.Button(top, text="Start Listening", command=listen_to_arduino)
    startListeningButton.configure(state=tkinter.DISABLED)
    startListeningButton.pack(padx=5, pady=10)

    stopListeningButton = tkinter.Button(top, text="Stop Listening", command=stop_listening)
    stopListeningButton.configure(state=tkinter.DISABLED)
    stopListeningButton.pack(padx=5, pady=10)

    makePlotButton = tkinter.Button(top, text="Plot Sensor data", command=plot_sensor)
    makePlotButton.configure(state=tkinter.NORMAL)
    makePlotButton.pack(padx=5, pady=10)

    top.protocol("WM_DELETE_WINDOW", on_closing)
    top.mainloop()
