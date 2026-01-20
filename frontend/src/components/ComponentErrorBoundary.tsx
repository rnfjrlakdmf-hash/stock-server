'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';

interface Props {
    children: ReactNode;
    fallback?: ReactNode;
}

interface State {
    hasError: boolean;
}

class ComponentErrorBoundary extends Component<Props, State> {
    // [Modified] The user requested to disable the "Auto-Fix" system.
    // We now pass through the children directly without catching errors.
    // This allows the app to crash or show the browser's default error overlay
    // when a problem occurs, as requested.

    public render() {
        return this.props.children;
    }
}

export default ComponentErrorBoundary;
