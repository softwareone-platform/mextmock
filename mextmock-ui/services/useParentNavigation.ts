/**
 * Hook to navigate the parent window to a new URL
 */
export const useParentNavigation = () => {
    const navigateParent = (path: string) => {
        try {
            // Try direct navigation if same-origin
            if (window.parent && window.parent !== window) {
                window.parent.history.pushState({}, '', path);

                // Trigger popstate event so parent app reacts to the change
                window.parent.dispatchEvent(new PopStateEvent('popstate'));

                console.log('Navigated parent to:', path);
            }
        } catch (e) {
            // Cross-origin - send message to parent
            console.log('Cross-origin detected, sending navigation message to parent');

            if (window.parent && window.parent !== window) {
                window.parent.postMessage({
                    type: 'NAVIGATE_REQUEST',
                    path: path
                }, '*'); // In production, replace '*' with specific origin
            }
        }
    };

    return { navigateParent };
};
