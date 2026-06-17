@echo off
:: Thiết lập mã hóa UTF-8 để hiển thị tiếng Việt có dấu trong Command Prompt
chcp 65001 >nul
title Khởi động Caro AI PRO

echo ===================================================
echo             KHỞI ĐỘNG TRÒ CHƠI CARO AI PRO         
echo ===================================================
echo.

:: 1. Kiểm tra Python đã cài đặt chưa
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI] Không tìm thấy Python trên hệ thống của bạn!
    echo Vui lòng tải và cài đặt Python (từ https://www.python.org) trước.
    echo.
    pause
    exit /b
)

:: 2. Kiểm tra và cài đặt pygame
echo [*] Đang kiểm tra thư viện pygame...
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo [THÔNG BÁO] Chưa cài đặt thư viện pygame hoặc các gói cần thiết.
    echo [*] Đang tự động cài đặt từ requirements.txt, vui lòng đợi...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [LỖI] Không thể cài đặt các thư viện. Vui lòng kiểm tra lại kết nối mạng.
        echo.
        pause
        exit /b
    )
    echo [+] Đã cài đặt xong các thư viện thành công!
    echo.
) else (
    echo [+] Thư viện pygame đã sẵn sàng.
)

:: 3. Khởi động trò chơi
echo [*] Đang khởi động trò chơi Caro AI PRO...
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [LỖI] Trò chơi kết thúc bất thường hoặc có lỗi xảy ra.
    pause
)
