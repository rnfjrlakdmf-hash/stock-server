import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  distDir: '.next_custom',
  output: 'export', // 안드로이드/iOS 앱 빌드(정적 내보내기)를 위해 활성화
  images: {
    unoptimized: true, // 정적 내보내기 시 이미지 최적화 비활성화 필수
  },
  // 웹 서버 헤더는 모바일 앱(정적 파일)에서는 무시됨
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cross-Origin-Opener-Policy',
            value: 'same-origin-allow-popups',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
