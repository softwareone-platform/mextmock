import { useAppContext } from '../../contexts/AppContext';

export const Page1 = () => {
    const { data } = useAppContext();

    return (
        <div>
            <h1>Page 1</h1>
            <p>This is the content for Page 1</p>
            {data?.url && (
                <p className="mono">
                  userId: {data.userId}
                </p>
            )}
        </div>
    );
};
