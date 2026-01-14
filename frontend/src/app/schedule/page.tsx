"use client";

import Header from "@/components/Header";
import MacroCalendar from "@/components/MacroCalendar";
import IPOCalendar from "@/components/IPOCalendar";

export default function SchedulePage() {
    return (
        <div className="min-h-screen pb-10 text-white">
            <Header title="증시 & 공모주 일정" subtitle="주요 경제 지표 발표 및 IPO 일정 확인" />

            <div className="p-6 space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Economic Calendar */}
                    <div className="space-y-4">
                        <MacroCalendar />
                    </div>

                    {/* IPO Calendar */}
                    <div className="space-y-4">
                        <IPOCalendar />
                    </div>
                </div>
            </div>
        </div>
    );
}
