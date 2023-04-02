from high_finesse import WavelengthMeter
path_to_dll = "C:\\Program Files (x86)\\HighFinesse\\Wavelength Meter WS Ultimate 1653\\Projects\\64\\wlmData.dll"

# initialize the wavelength meter
# wlm = WavlengthMeter(dllpath="C:\Windows\System32\wlmData.dll")  # this is also the default
wlm = WavelengthMeter(dllpath="C:\\Program Files (x86)\\HighFinesse\\Wavelength Meter WS Ultimate 1653\\Projects\\64\\wlmData.dll")
print(wlm.wavelengths)  # reads all wavelengths in a list

ch3 = wlm.channel[2]  # count pythonic!
ch3.use_channel = True
ch3.auto_exposure = True
print(ch3.frequency)