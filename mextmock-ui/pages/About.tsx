import { useMPTContext } from "@mpt-extension/sdk-react";
import { useMemo } from "react";

export default () => {
    const { auth, data } = useMPTContext();

    const contextAuthSnapshot = useMemo(() => {
        if (!auth) return [];
        return Object.keys(auth).map(k => [k, auth[k]?.id ?? JSON.stringify(auth[k])])
    }, [data]);

    return <div>
        <h1>About</h1>
        <p>This is the mextmock extension UI.</p>
        <p className="mono">
            {contextAuthSnapshot.map(([key, value]) => <>{`${key}: ${value}`}<br /></>)}
        </p>
    </div>
};