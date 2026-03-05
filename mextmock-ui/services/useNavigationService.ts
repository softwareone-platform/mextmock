import { useState, useCallback, useEffect } from 'react';
import { useAppContext } from '../contexts/AppContext';
import { getRouteFromUrl } from './useParentUrl';
import { useParentNavigation } from './useParentNavigation';

export type Route = 'home' | 'page1' | 'page2';

/**
 * Navigation Service Hook
 * Manages routing state and navigation logic for the application
 */
export const useNavigationService = () => {
    const { data } = useAppContext();
    const contextUrl = data?.url || '';
    const initialRoute = getRouteFromUrl(contextUrl);
    const [route, setRoute] = useState<Route>(initialRoute as Route);
    const { navigateParent } = useParentNavigation();

    // Update route when context URL changes
    useEffect(() => {
        const newRoute = getRouteFromUrl(contextUrl);
        if (newRoute !== route) {
            setRoute(newRoute as Route);
        }
    }, [contextUrl]);

    const navigate = useCallback((page: Route) => {
        // Update local state immediately for responsive UI
        setRoute(page);

        // Update parent URL
        const basePath = 'https://portal.s1.show/home';
        const newPath = page === 'home' ? basePath : `${basePath}/${page}`;
        navigateParent(newPath);
    }, [navigateParent]);

    return {
        currentRoute: route,
        navigate
    };
};
