tasklist /fi "imagename eq btsync.exe" | find ":" > nul
if errorlevel 1 taskkill /f /im "btsync.exe"
.\\bin\\btsync\\btsync.exe /config btsync.conf