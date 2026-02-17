import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useMPTContext } from "@mpt-extension/sdk-react";
import { useMemo } from "react";
export default () => {
    const { auth, data } = useMPTContext();
    const contextAuthSnapshot = useMemo(() => {
        if (!auth)
            return [];
        return Object.keys(auth).map(k => [k, auth[k]?.id ?? JSON.stringify(auth[k])]);
    }, [data]);
    return _jsxs("div", { children: [_jsx("h1", { children: "About" }), _jsx("p", { children: "This is the mextmock extension UI." }), _jsx("p", { className: "mono", children: contextAuthSnapshot.map(([key, value]) => _jsxs(_Fragment, { children: [`${key}: ${value}`, _jsx("br", {})] })) })] });
};
