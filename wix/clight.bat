set VERSION=0.3
pushd wix
del aksy-%VERSION%.msi
build_wix.py
candle -v aksy-installer.wxs -out aksy-installer.wixobj
light aksy-installer.wixobj -ext WixUIExtension -out aksy-%VERSION%.msi -cultures:en-us
popd
