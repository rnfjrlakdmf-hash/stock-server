export const checkReward = (): boolean => {
    if (typeof window === 'undefined') return false;

    // Pro User Check
    const isPro = localStorage.getItem("isPro") === "true";
    if (isPro) return true;

    // Time-based Reward Check
    const expiry = localStorage.getItem("rewardExpiry");
    if (expiry) {
        if (parseInt(expiry) > Date.now()) {
            return true;
        }
        // Expired
        localStorage.removeItem("rewardExpiry");
    }
    return false;
};

export const grantReward = (minutes: number) => {
    const now = Date.now();
    // Add time to existing expiry if valid, else start from now
    const currentExpiry = localStorage.getItem("rewardExpiry");
    let baseTime = now;
    if (currentExpiry && parseInt(currentExpiry) > now) {
        baseTime = parseInt(currentExpiry);
    }

    const newExpiry = baseTime + (minutes * 60 * 1000);
    localStorage.setItem("rewardExpiry", newExpiry.toString());
};

export const getRewardTimeLeft = (): string => {
    if (typeof window === 'undefined') return "";
    const expiry = localStorage.getItem("rewardExpiry");
    if (!expiry) return "";

    const diff = parseInt(expiry) - Date.now();
    if (diff <= 0) return "";

    const minutes = Math.ceil(diff / 60000);
    if (minutes > 60) {
        const h = Math.floor(minutes / 60);
        const m = minutes % 60;
        return `${h}시간 ${m}분`;
    }
    return `${minutes}분`;
};
