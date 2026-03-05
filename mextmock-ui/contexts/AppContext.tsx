import { createContext, useContext, ReactNode } from 'react';
import { useMPTContext } from '@mpt-extension/sdk-react';

/**
 * Global Application Context
 * Provides access to MPT context (auth, data) throughout the app
 */

interface User {
    id: string;
}

interface Account {
    id: string;
    type: string;
}

interface AuthData {
    user: User;
    account: Account;
}

interface ContextData {
    userId: string;
    language: string;
    url: string;
}

interface AppContextData {
    auth: AuthData | null;
    data: ContextData | null;
}

const AppContext = createContext<AppContextData | undefined>(undefined);

interface AppContextProviderProps {
    children: ReactNode;
}

/**
 * AppContextProvider - Wraps the app to provide global context
 */
export const AppContextProvider = ({ children }: AppContextProviderProps) => {
    const { auth, data } = useMPTContext();
    return (
        <AppContext.Provider value={{ auth, data }}>
            {children}
        </AppContext.Provider>
    );
};

/**
 * useAppContext - Hook to access global context from any component
 *
 * @returns {AppContextData} { auth, data }
 * @throws {Error} If used outside AppContextProvider
 *
 * @example
 * const { auth, data } = useAppContext();
 * console.log('Current URL:', data?.url);
 */
export const useAppContext = (): AppContextData => {
    const context = useContext(AppContext);

    if (context === undefined) {
        throw new Error('useAppContext must be used within AppContextProvider');
    }

    return context;
};
