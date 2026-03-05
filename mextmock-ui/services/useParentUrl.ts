import { useState, useEffect } from 'react';

export const useParentUrl = () => {
    const [parentUrl, setParentUrl] = useState<string>('');

    useEffect(() => {
        // Get initial parent URL
        try {
            if (window.parent && window.parent !== window) {
                setParentUrl(window.parent.location.href);

                console.log(window.parent)
            }
        } catch (e) {
            // Cross-origin restrictions - listen to messages instead
            console.log('Cannot access parent URL directly, listening for messages');
        }

        // Listen for URL changes from parent
        const handleMessage = (event: MessageEvent) => {
            // Optional: Verify origin for security
            // Uncomment and set your parent origin in production
            // const allowedOrigin = 'https://portal.s1.show';
            // if (event.origin !== allowedOrigin) {
            //     console.warn('Ignored message from unknown origin:', event.origin);
            //     return;
            // }

            if (event.data && event.data.type === 'URL_CHANGE') {
                console.log('Received URL change from parent:', event.data.url);
                setParentUrl(event.data.url);
            }
        };

        window.addEventListener('message', handleMessage);

        // Also listen for hash changes and popstate in parent
        const checkParentUrl = () => {
            try {
                if (window.parent && window.parent !== window) {
                    setParentUrl(window.parent.location.href);
                }
            } catch (e) {
                // Silently fail if cross-origin
            }
        };

        // Poll for URL changes as fallback
        const interval = setInterval(checkParentUrl, 500);

        return () => {
            window.removeEventListener('message', handleMessage);
            clearInterval(interval);
        };
    }, []);

    return parentUrl;
};

export const getRouteFromUrl = (url: string): string => {
    if (!url) return 'home';

    try {
        const urlObj = new URL(url);
        const pathname = urlObj.pathname;

        // Extract route from pathname
        // e.g., /home -> 'home', /home/page1 -> 'page1', /home/page2 -> 'page2'
        const segments = pathname.split('/').filter(Boolean);

        // If we have at least 2 segments (e.g., ['home', 'page1']), return the last one
        // Otherwise return 'home'
        if (segments.length >= 2) {
            return segments[segments.length - 1];
        }

        return 'home';
    } catch (e) {
        return 'home';
    }
};
