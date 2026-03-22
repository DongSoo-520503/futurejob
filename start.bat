@echo off
:: 브라우저에서 5500 포트로 접속
start http://127.0.0.1:5500
:: 서버를 5500 포트로 실행
npx http-server -p 5500
pause