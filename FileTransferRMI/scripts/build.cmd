@echo off
echo Building the RMI File Transfer Project...

rem Compile common source
javac -d common/bin common/src/*.java

rem Compile client source (include common in classpath)
javac -cp common/bin -d client/bin client/src/*.java

rem Compile server source (include common in classpath)
javac -cp common/bin -d server/bin server/src/*.java

echo Build completed.
pause
