import { useAppContext } from '../../contexts/AppContext';

export const Page2 = () => {
    const { auth, data } = useAppContext();

    return (
        <div>
            <h1>Page 2</h1>
            <p>This is the content for Page 2</p>
            {auth && (
                <p className="mono">
                    Auth available: {Object.keys(auth).length} properties
                </p>
            )}
            {data?.url && (
                <p className="mono">
                    Current URL: {data.url}
                </p>
            )}
        </div>
    );
};
