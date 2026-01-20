"use client";

import { useState, useEffect } from "react";
import { X, Play, Loader2, Coins, Zap, Timer, CheckCircle2 } from "lucide-react";
import { requestPayment } from "@/lib/payment";
import { API_BASE_URL } from "@/lib/config";
import { grantReward } from "@/lib/reward";

interface AdModalProps {
    isOpen: boolean;
    onClose: () => void;
    onReward: () => void;
    featureName: string;
}

const REWARD_OPTIONS = [
    { count: 5, time: 30, label: "30분 이용권 (광고 5회)" },
    { count: 10, time: 120, label: "2시간 이용권 (광고 10회)", badge: "BEST" },
    { count: 15, time: 180, label: "3시간 이용권 (광고 15회)", badge: "MAX" },
];

export default function AdRewardModal({ isOpen, onClose, onReward, featureName }: AdModalProps) {
    const [isPlaying, setIsPlaying] = useState(false);
    const [timeLeft, setTimeLeft] = useState(5);
    const [progress, setProgress] = useState(0); // 현재 시청 횟수 (0 ~ target)
    const [targetCount, setTargetCount] = useState(1); // 목표 시청 횟수
    const [targetRewardTime, setTargetRewardTime] = useState(0); // 목표 보상 시간 (분)
    const [exchangeRate, setExchangeRate] = useState<number>(1450);

    useEffect(() => {
        if (isOpen) {
            // Reset state on open
            setProgress(0);
            setIsPlaying(false);
            setTargetCount(1);

            fetch(`${API_BASE_URL}/api/market/status`)
                .then(res => res.json())
                .then(data => {
                    if (data.status === "success" && data.data.details?.usd) {
                        const rate = parseFloat(data.data.details.usd.replace(/,/g, ''));
                        if (!isNaN(rate)) setExchangeRate(rate);
                    }
                })
                .catch(err => console.error(err));
        }
    }, [isOpen]);

    useEffect(() => {
        let timer: NodeJS.Timeout;
        if (isPlaying && timeLeft > 0) {
            timer = setInterval(() => {
                setTimeLeft((prev) => prev - 1);
            }, 1000);
        } else if (isPlaying && timeLeft === 0) {
            // 광고 1회 종료
            setTimeout(() => {
                const nextProgress = progress + 1;
                setProgress(nextProgress);

                if (nextProgress >= targetCount) {
                    // 목표 달성!
                    grantReward(targetRewardTime);
                    onReward(); // 상위 컴포넌트 알림
                    setIsPlaying(false);
                    onClose(); // 닫기
                    alert(`${targetRewardTime}분 무료 이용권이 지급되었습니다!`);
                } else {
                    // 다음 광고 준비
                    setTimeLeft(5); // 다시 5초
                    // 잠시 대기 후 바로 재생 or 사용자 클릭? -> 연속 재생 (사용자 편의)
                    // setIsPlaying(true); // 이미 true지만 리셋 필요할 수 있음
                }
            }, 500);
        }
        return () => clearInterval(timer);
    }, [isPlaying, timeLeft, onReward, progress, targetCount, targetRewardTime, onClose]);

    const startAdLoop = () => {
        setTargetCount(5);
        setTargetRewardTime(30);
        setProgress(0);
        setTimeLeft(5);
        setIsPlaying(true);
    };

    const proPriceUsd = 3.5;
    const proPriceKrw = Math.floor(proPriceUsd * exchangeRate / 10) * 10;

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
            {isPlaying ? (
                // 광고 재생 화면
                <div className="bg-white text-black w-full max-w-sm aspect-[9/16] rounded-xl relative overflow-hidden flex flex-col items-center justify-center shadow-2xl animate-in zoom-in duration-300">
                    <div className="absolute top-4 right-4 bg-black/50 text-white px-3 py-1 rounded-full text-xs font-bold z-10">
                        Ad {progress + 1}/{targetCount} : {timeLeft}s
                    </div>

                    {/* Progress Bar for Multi-ad */}
                    <div className="absolute top-0 left-0 w-full h-1 bg-gray-200 z-20">
                        <div
                            className="h-full bg-green-500 transition-all duration-300"
                            style={{ width: `${(progress / targetCount) * 100}%` }}
                        />
                    </div>

                    <div className="text-center p-6 space-y-4 animate-in zoom-in duration-500">
                        <div className="w-20 h-20 bg-blue-500 rounded-xl mx-auto flex items-center justify-center text-white font-black text-2xl shadow-xl">
                            AD
                        </div>
                        <h3 className="text-xl font-bold">Awesome Promotion {progress + 1}</h3>
                        <p className="text-gray-500 text-sm">Watching ad {progress + 1} of {targetCount}...</p>
                        <div className="flex justify-center gap-1 mt-2">
                            {[...Array(targetCount)].map((_, i) => (
                                <div key={i} className={`w-2 h-2 rounded-full ${i < progress ? 'bg-green-500' : i === progress ? 'bg-blue-500 animate-pulse' : 'bg-gray-300'}`} />
                            ))}
                        </div>
                    </div>

                    <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-200">
                        <div
                            className="h-full bg-blue-600 transition-all duration-1000 ease-linear"
                            style={{ width: `${((5 - timeLeft) / 5) * 100}%` }}
                        />
                    </div>
                </div>
            ) : (
                // 단일 미션 화면
                <div className="bg-gray-900 border border-white/10 w-full max-w-md rounded-[2rem] p-6 text-center shadow-2xl relative animate-in fade-in zoom-in-95 duration-300 flex flex-col max-h-[90vh] overflow-y-auto">
                    <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-white z-10">
                        <X className="w-6 h-6" />
                    </button>

                    <div className="mb-4 flex justify-center">
                        <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg shadow-blue-500/20 animate-pulse">
                            <Timer className="w-10 h-10 text-white" />
                        </div>
                    </div>

                    <h2 className="text-2xl font-black text-white mb-1">
                        Get Free 30 Mins
                    </h2>
                    <p className="text-gray-400 mb-8 text-sm leading-relaxed">
                        광고 5편 시청하고 <span className="text-yellow-400 font-bold">30분 무료 이용권</span>을 충전하세요!<br />
                        (반복 참여 가능)
                    </p>

                    <button
                        onClick={startAdLoop}
                        className="w-full relative group overflow-hidden bg-white hover:bg-gray-100 rounded-xl p-5 transition-all active:scale-95 shadow-lg shadow-white/10 mb-6"
                    >
                        <div className="flex items-center justify-between">
                            <div className="text-left">
                                <div className="font-black text-black text-lg">30분 충전하기</div>
                                <div className="text-xs text-gray-500">대기 중인 광고 5개</div>
                            </div>
                            <div className="bg-black text-white p-3 rounded-full group-hover:bg-blue-600 transition-colors">
                                <Play className="w-6 h-6 fill-current" />
                            </div>
                        </div>
                    </button>

                    <div className="pt-6 border-t border-white/5 space-y-3">
                        <button
                            onClick={() => {
                                requestPayment(() => {
                                    localStorage.setItem("isPro", "true");
                                    alert("결제가 완료되었습니다! 프로 기능이 활성화됩니다.");
                                    window.location.reload();
                                });
                            }}
                            className="w-full py-3 bg-gradient-to-r from-gray-800 to-gray-700 text-gray-300 rounded-xl font-bold text-sm hover:text-white transition-all flex items-center justify-center gap-2"
                        >
                            <Zap className="w-4 h-4" /> 귀찮으신가요? 평생 소장하기 (${proPriceUsd})
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
