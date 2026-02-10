import {useMemo, useCallback, useState} from 'react';
import { useMPTContext, useMPTModal } from '@mpt-extension/sdk-react';

import './styles.scss';

export default () => {
    const { auth, data } = useMPTContext();
    const { open, close } = useMPTModal();

    const openModal = useCallback(() => {
        open('modal', {
            context: {
                ...data,
                isOpenedAsModal: 'TRUE',
            },

            onClose: (data) => {
                console.log(`📢 Requested modal was closed with ${JSON.stringify(data)}`);
            },
        });
    }, [open, data]);

    const closeModal = useCallback((key) => {
        close(key);
    }, [close]);

    const contextAuthSnapshot = useMemo(() => {
        if (!auth) return [];
        return Object.keys(auth).map(k => [k, auth[k]?.id ?? JSON.stringify(auth[k])])
    }, [data]);

    const contextDataSnapshot = useMemo(() => {
        if (!data) return [];
        return Object.keys(data).map(k => [k, data[k]?.id ?? JSON.stringify(data[k])])
    }, [data]);

    return <div className='container'>
        <h1>A brave lil extension</h1>

        <h3>{contextAuthSnapshot.length ? 'You are browsing extension as:' : 'Your identity is undetected' }</h3>
        <p className="mono">
            {contextAuthSnapshot.map(([key, value]) => <>{`${key}: ${value}`}<br /></>)}
        </p>

        <h3>{contextDataSnapshot.length ? 'You are in context of:' : 'There is no meaningful context' }</h3>
        <p className="mono">
            {contextDataSnapshot.map(([key, value]) => <>{`${key}: ${value}`}<br /></>)}
        </p>

        <div className='row'>
            <button onClick={openModal}>Open modal</button>
            <button onClick={() => closeModal('foo')}>Say FOO</button>
            <button onClick={() => closeModal('bar')}>Say BAR </button>
        </div>
    </div>
};