import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useMemo, useCallback } from 'react';
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
        if (!auth)
            return [];
        return Object.keys(auth).map(k => [k, auth[k]?.id ?? JSON.stringify(auth[k])]);
    }, [data]);
    const contextDataSnapshot = useMemo(() => {
        if (!data)
            return [];
        return Object.keys(data).map(k => [k, data[k]?.id ?? JSON.stringify(data[k])]);
    }, [data]);
    return _jsxs("div", { className: 'container', children: [_jsx("h1", { children: "A brave lil extension" }), _jsx("h3", { children: contextAuthSnapshot.length ? 'You are browsing extension as:' : 'Your identity is undetected' }), _jsx("p", { className: "mono", children: contextAuthSnapshot.map(([key, value]) => _jsxs(_Fragment, { children: [`${key}: ${value}`, _jsx("br", {})] })) }), _jsx("h3", { children: contextDataSnapshot.length ? 'You are in context of:' : 'There is no meaningful context' }), _jsx("p", { className: "mono", children: contextDataSnapshot.map(([key, value]) => _jsxs(_Fragment, { children: [`${key}: ${value}`, _jsx("br", {})] })) }), _jsxs("div", { className: 'row', children: [_jsx("button", { onClick: openModal, children: "Open modal" }), _jsx("button", { onClick: () => closeModal('foo'), children: "Say FOO" }), _jsx("button", { onClick: () => closeModal('bar'), children: "Say BAR " })] })] });
};
