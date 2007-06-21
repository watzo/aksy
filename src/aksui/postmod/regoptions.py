
import _winreg, traceback

def getInstallPath():
    reg = key = path = None
    try:
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        key = _winreg.OpenKey(reg, r"Software\Magicfish Software\Magicfish Postmod 2.0", 0, _winreg.KEY_READ)
        path, tp = _winreg.QueryValueEx(key, "InstallPath")
    except:
        path = None
    if key:
        key.Close()
    if reg:
        reg.Close()

    if not path:
        reg = key = path = None
        try:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
            key = _winreg.OpenKey(reg, r"Software\Magicfish Software\Magicfish Postmod 2.0", 0, _winreg.KEY_READ)
            path, tp = _winreg.QueryValueEx(key, "InstallPath")
        except:
            path = None
        if key:
            key.Close()
        if reg:
            reg.Close()

    if path:
        path = str(path)

    return path

if __name__ == "__main__":
    print getInstallPath()

    