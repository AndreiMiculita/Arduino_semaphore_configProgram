import tkinter
import tkinter.messagebox
import serial
import serial.tools.list_ports

ports = ["Choose a port"]
ser = serial.Serial()


def choose_port():
    ser.port = chosen_port.get()
    try:
        ser.open()
        tkinter.messagebox.showinfo("Port Set", "Port Set")
    except Exception as e:
        tkinter.messagebox.showinfo("Port Set", str(e))
        exit()


def send_message():
    print("message sent a" + interval_entry1.get() + ":"
          + interval_entry2.get() + ":"
          + interval_entry3.get() + ":"
          + interval_entry4.get())


if __name__ == '__main__':
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
    sendMessageButton.pack(padx=5, pady=10)

    top.mainloop()
