echo off
cls
set count=0

:start
echo Connection attempt %count%
kamikaze_bot.py
for /l %%x in (30, -1, 1) do cls & echo Reconnecting in %%x... & ping -n 2 127.0.0.1 > NUL
set /a count=%count%+1
goto start