import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.rnfjr.stockai',
  appName: 'AI Stock Analyst',
  webDir: '.next_custom',
  server: {
    androidScheme: 'http',
    cleartext: true
  }
};

export default config;
