'use client'; // Error boundaries must be Client Components

import { useEffect } from 'react';
import { Loader2, RefreshCw, Home } from 'lucide-react';

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        // 에러 로그 출력
        console.error('Error Boundary Caught:', error);
    }, [error]);

    return (
        <div className="flex h-screen flex-col items-center justify-center bg-[#09090b] text-white p-6 text-center animate-in fade-in duration-500 overflow-y-auto">
            <div className="bg-red-500/10 p-4 rounded-full mb-6 ring-4 ring-red-500/20">
                <RefreshCw className="w-12 h-12 text-red-500" />
            </div>

            <h2 className="text-2xl font-black text-white mb-2 tracking-tight">
                시스템 오류가 발생했습니다
            </h2>

            <p className="text-gray-400 mb-8 max-w-xs text-sm leading-relaxed">
                일시적인 오류일 수 있습니다. 아래 버튼을 눌러 다시 시도해보세요.
            </p>

            <div className="flex flex-col gap-3 w-full max-w-xs mb-8">
                <button
                    className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 px-6 rounded-xl transition-all shadow-lg shadow-blue-900/50 flex items-center justify-center gap-2 active:scale-95"
                    onClick={() => reset()}
                >
                    <RefreshCw className="w-4 h-4" />
                    다시 시도
                </button>

                <button
                    className="w-full bg-white/5 hover:bg-white/10 text-gray-300 font-bold py-4 px-6 rounded-xl transition-all border border-white/10 flex items-center justify-center gap-2"
                    onClick={() => window.location.href = '/'}
                >
                    <Home className="w-4 h-4" />
                    홈 화면으로 이동
                </button>
            </div>

            <div className="w-full max-w-sm text-left">
                <p className="text-xs text-gray-500 mb-2 font-mono text-center">Reference Code: {error.digest || "UNKNOWN_ERR"}</p>

                {/* Detailed Debug Info */}
                <div className="bg-black/50 p-4 rounded-xl border border-red-500/30 text-red-300 text-[10px] font-mono overflow-x-auto whitespace-pre-wrap max-h-60 custom-scrollbar shadow-inner">
                    <p className="font-bold border-b border-red-500/30 pb-2 mb-2 text-red-400">Error Details:</p>
                    <p className="mb-2">{error.message || "No error message available"}</p>
                    {error.stack && (
                        <div className="opacity-70 mt-4 pt-4 border-t border-red-500/10">
                            <p className="font-bold mb-1">Stack Trace:</p>
                            {error.stack.split('\n').slice(0, 10).map((line, i) => (
                                <div key={i} className="pl-2 border-l-2 border-white/10 mb-0.5">{line}</div>
                            ))}
                        </div>
                    )}
                </div>
                <p className="text-[10px] text-gray-600 mt-2 text-center">
                    * 위 에러 메시지를 캡처하여 개발자에게 전달해주세요.
                </p>
            </div>
        </div>
    );
}
