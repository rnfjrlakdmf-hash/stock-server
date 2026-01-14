@echo off
echo [StockTrend] 외부 접속을 위한 방화벽 설정을 추가합니다...
echo (관리자 권한으로 실행해야 합니다)

netsh advfirewall firewall add rule name="StockTrend Frontend (3000)" dir=in action=allow protocol=TCP localport=3000
netsh advfirewall firewall add rule name="StockTrend Backend (8000)" dir=in action=allow protocol=TCP localport=8000

echo.
echo 설정이 완료되었습니다!
echo 이제 다른 기기(스마트폰, 노트북 등)에서 아래 주소로 접속해보세요:
echo.
ipconfig | findstr "IPv4"
echo.
echo (포트는 3000번입니다. 예: http://192.168.0.x:3000)
pause
