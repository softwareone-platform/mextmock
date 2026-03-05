import { useMemo } from 'react';
import { useAppContext } from '../../contexts/AppContext';

export const Home = () => {
    const { auth, data } = useAppContext();

    const contextAuthSnapshot = useMemo(() => {
        if (!auth) return [];
        return Object.keys(auth).map(k => [k, auth[k]?.id ?? JSON.stringify(auth[k])]);
    }, [auth]);

    const contextDataSnapshot = useMemo(() => {
        if (!data) return [];
        return Object.keys(data).map(k => [k, data[k]?.id ?? JSON.stringify(data[k])]);
    }, [data]);

    return (
        <>
            <h1>A brave lil extension 1 - new plug</h1>

            <h3>{contextAuthSnapshot.length ? 'You are browsing extension as:' : 'Your identity is undetected'}</h3>
            <p className="mono">
                {contextAuthSnapshot.map(([key, value]) => <>{`${key}: ${value}`}<br/></>)}
            </p>

            <h3>{contextDataSnapshot.length ? 'You are in context of:' : 'There is no meaningful context'}</h3>
            <p className="mono">
                {contextDataSnapshot.map(([key, value]) => <>{`${key}: ${value}`}<br/></>)}
            </p>
        </>
    );
};
