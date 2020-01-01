from powerchute_be_web_api import PowerChute

default_port = "6547"
myups = PowerChute("your ip address here",default_port,"your username here","your password here")

print("charge: " + str(myups.get_battery_charge()) + "%")
print("input voltage: " + str(myups.get_input_voltage()) + "v")
print("status: " + myups.get_field_by_html_id("value_DeviceStatus"))
