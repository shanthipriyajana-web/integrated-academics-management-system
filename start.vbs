Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd /d ""D:\major project\Integrated_academics_management_system"" && python manage.py runserver 127.0.0.1:8000", 0, False
WScript.Sleep 3000
WshShell.Run "http://127.0.0.1:8000"