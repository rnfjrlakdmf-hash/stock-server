$ErrorActionPreference = "Stop"

Write-Host "🚀 모바일 앱 업데이트를 시작합니다..." -ForegroundColor Cyan

# 1. Frontend 폴더로 이동
Set-Location "$PSScriptRoot\frontend"

# 2. Next.js 빌드 (새로운 코드를 웹사이트로 만들기)
Write-Host "📦 1단계: 최신 코드로 다시 포장하는 중... (잠시만 기다려주세요)" -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ 빌드 중 오류가 발생했습니다."

    exit
}

# 3. Capacitor 동기화 (앱으로 내보내기)
Write-Host "🔄 2단계: 안드로이드 앱으로 변환 중..." -ForegroundColor Yellow
npx cap sync
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ 동기화 중 오류가 발생했습니다."

    exit
}

# 4. 안드로이드 스튜디오 열기 or 실행
Write-Host "📲 3단계: 핸드폰에 설치 준비 완료!" -ForegroundColor Green
Write-Host "안드로이드 스튜디오가 열리면 '▶ (재생)' 버튼을 눌러주세요." -ForegroundColor Cyan

# 우선 실행을 시도해보고, 안되면 스튜디오를 엽니다.
# npx cap run android 

npx cap open android

Write-Host "✅ 모든 준비가 끝났습니다." -ForegroundColor Green
Start-Sleep -Seconds 5
