# 주식 분석 프로그램 모바일 앱(Android/iOS) 변환 가이드

네, 현재 만드신 웹 프로그램을 **Android(갤럭시)**와 **iOS(아이폰)** 앱으로 만드는 것은 충분히 가능합니다!

우리는 **Capacitor**라는 기술을 사용할 것입니다. 이 기술은 현재의 Next.js 웹사이트를 그대로 모바일 앱으로 포장(Wrapping)해주는 도구입니다.

## 🏗️ 전체 구조 (아키텍처)

모바일 앱으로 전환할 때 가장 중요한 점은 **'백엔드(파이썬)'의 위치**입니다.

*   **📱 앱 (프론트엔드)**: 사용자의 핸드폰에 설치됩니다. (Next.js 화면)
*   **☁️ 서버 (백엔드)**: 파이썬(FastAPI) 프로그램은 핸드폰 안에서 돌아가지 않습니다. **별도의 서버(컴퓨터/클라우드)**에 켜져 있어야 합니다.
*   **통신**: 앱은 인터넷을 통해 서버에 데이터를 요청합니다.

> **💡 핵심**: 앱을 출시하려면 파이썬 백엔드를 AWS, Google Cloud 같은 서버에 올려야 합니다. (지금 당장 테스트할 때는 PC를 서버로 쓸 수 있습니다.)

---

## 🚀 1단계: 준비물

1.  **Android 앱 빌드**: [Android Studio](https://developer.android.com/studio) 설치 필요
2.  **iOS 앱 빌드**: Mac 컴퓨터와 [Xcode](https://developer.apple.com/xcode/) 설치 필요 (Windows에서는 iOS 빌드가 불가능합니다 😢)

---

## 🛠️ 2단계: 프로젝트에 Capacitor 설치

터미널에서 다음 명령어들을 순서대로 실행하여 모바일 기능을 추가합니다.

```bash
# 1. Capacitor 라이브러리 설치
npm install @capacitor/core
npm install -D @capacitor/cli

# 2. Capacitor 초기화 (앱 이름 및 ID 설정)
# npx cap init [앱이름] [고유ID]
npx cap init "StockAI" "com.stockai.app"

# 3. 안드로이드/iOS 플랫폼 추가
npm install @capacitor/android @capacitor/ios
npx cap add android
npx cap add ios
```

---

## ⚙️ 3단계: Next.js 설정 변경

앱은 서버 없이 파일로 실행되므로, Next.js를 **Static Export(정적 내보내기)** 모드로 변경해야 합니다.

`next.config.js` 파일을 열어 다음 설정을 추가합니다:

```javascript
/* next.config.js */
const nextConfig = {
  output: 'export',  // 이 줄을 추가! (정적 파일로 빌드)
  images: {
    unoptimized: true, // 이미지 최적화 기능 끄기 (앱에서는 필수)
  },
  // ... 기존 설정들
};
```

---

## 📦 4단계: 빌드 및 앱 만들기

이제 웹 코드를 모바일 앱용 코드로 변환합니다.

```bash
# 1. Next.js 빌드 (out 폴더가 생성됨)
npm run build

# 2. 빌드된 내용을 모바일 프로젝트로 복사
npx cap sync
```

---

## 📱 5단계: 실행 및 테스트

```bash
# 안드로이드 스튜디오 열기
npx cap open android

# (Mac 사용자용) Xcode 열기
npx cap open ios
```

열리는 프로그램(Android Studio 등)에서 `Play` 버튼(▶)을 누르면 시뮬레이터나 연결된 휴대폰에서 앱이 실행됩니다!

---

## ⚠️ 주의사항: API 주소 변경

현재 코드에서 `API_BASE_URL`이 `http://localhost:8000`으로 되어 있다면, 핸드폰에서는 접속이 안 됩니다.
(핸드폰 입장에서 localhost는 핸드폰 자신을 의미하기 때문입니다.)

1.  **테스트 할 때**: PC의 IP 주소(예: `http://192.168.0.5:8000`)를 입력해야 합니다.
2.  **실제 배포 할 때**: 클라우드 서버 주소(예: `https://api.mystockapp.com`)로 변경해야 합니다.

---

### ❓ 지금 바로 시작할까요?
원하시면 제가 **2단계(Capacitor 설치)**와 **3단계(설정 변경)**를 바로 진행해 드릴 수 있습니다. 진행하시겠습니까?
