@echo off
echo Starting RMI File Transfer Server...
java -cp server/bin;common/bin server.src.MainServer
pause
