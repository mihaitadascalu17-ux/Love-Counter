$scriptPath = "C:\tracker_cheltuieli\start_love_app.bat"
$shortcutPath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\LoveCounter.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $scriptPath
$Shortcut.WorkingDirectory = "C:\tracker_cheltuieli"
$Shortcut.Save()

Write-Host "✅ Love Counter se va porni automat la startup!"
