"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { X, User as UserIcon } from "lucide-react";
import { useGoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";

interface LoginModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export default function LoginModal({ isOpen, onClose }: LoginModalProps) {
    const { login } = useAuth();
    const [errorMsg, setErrorMsg] = useState("");

    const handleGoogleLogin = () => {
        // Direct Redirect to Google OAuth 2.0
        const client_id = "385839147502-p66mmuojl8g3vmclmvdqj54a3hk677nr.apps.googleusercontent.com";
        const redirect_uri = window.location.origin; // e.g. http://localhost:3000
        // Implicit Flow: response_type=token
        const url = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${client_id}&redirect_uri=${encodeURIComponent(redirect_uri)}&response_type=token&scope=email%20profile%20openid&include_granted_scopes=true&enable_serial_consent=true`;

        window.location.href = url;
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <div className="relative bg-[#111] border border-white/20 rounded-3xl w-full max-w-sm overflow-hidden shadow-2xl">
                <div className="absolute top-4 right-4">
                    <button onClick={onClose} className="text-gray-400 hover:text-white">
                        <X size={20} />
                    </button>
                </div>

                <div className="p-8 text-center">
                    <div className="w-12 h-12 bg-blue-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                        <UserIcon className="w-6 h-6 text-white" />
                    </div>
                    <h2 className="text-xl font-bold text-white mb-2">로그인</h2>
                    <p className="text-sm text-gray-400 mb-8">
                        개인화된 포트폴리오 관리를 위해 로그인하세요.
                    </p>

                    <div className="w-full max-w-[240px] flex flex-col gap-3 justify-center mx-auto">
                        <button
                            onClick={handleGoogleLogin}
                            className="w-full py-3 rounded-full bg-white text-black font-bold text-sm hover:bg-gray-100 transition-colors flex items-center justify-center gap-2"
                        >
                            <svg width="20" height="20" viewBox="0 0 24 24">
                                <path
                                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                                    fill="#4285F4"
                                />
                                <path
                                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                    fill="#34A853"
                                />
                                <path
                                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.26.81-.58z"
                                    fill="#FBBC05"
                                />
                                <path
                                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                    fill="#EA4335"
                                />
                            </svg>
                            Google 계정으로 계속하기
                        </button>

                        <div className="relative flex py-2 items-center">
                            <div className="flex-grow border-t border-gray-700"></div>
                            <span className="flex-shrink-0 mx-4 text-gray-500 text-xs">또는</span>
                            <div className="flex-grow border-t border-gray-700"></div>
                        </div>

                        <button
                            onClick={async () => {
                                const devUser = {
                                    id: "dev_" + Math.random().toString(36).substring(7),
                                    email: "demo@stocktrend.ai",
                                    name: "DemoUser",
                                    picture: "",
                                    token: "demo_token"
                                };
                                const success = await login(devUser);
                                if (success) window.location.reload();
                            }}
                            className="w-full py-2.5 rounded-full bg-white/5 hover:bg-white/10 text-gray-300 text-sm font-medium transition-all border border-white/10 flex items-center justify-center gap-2"
                        >
                            🚀 체험용 계정으로 로그인 (빠른실행)
                        </button>
                    </div>
                </div>

                {errorMsg && (
                    <p className="text-red-400 text-xs mt-4">{errorMsg}</p>
                )}

                <div className="text-xs text-gray-500 mt-6">
                    * 구글 계정으로 안전하게 로그인됩니다.<br />
                    별도의 회원가입 절차가 없습니다.
                </div>
            </div>
        </div>
    );
}
