
# get vst plugins path from registry
#My Computer\HKEY_LOCAL_MACHINE\SOFTWARE\VST\VSTPluginsPath = C:\Program Files\Steinberg\VstPlugIns

import _winreg, traceback

def getVSTPath():
    try:
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        key = _winreg.OpenKey(reg, r"SOFTWARE\VST", 0, _winreg.KEY_READ)
        value, type = _winreg.QueryValueEx(key, "VSTPluginsPath")
        _winreg.CloseKey(key)
        _winreg.CloseKey(reg)
        return value
    except:
        #traceback.print_exc()
        return "C:\\Program Files\\Steinberg\\VstPlugIns"
    

if __name__ == "__main__":
    print getVSTPath()


