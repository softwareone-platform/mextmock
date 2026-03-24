import {useCallback, useState, useEffect } from 'react';
import { Routes, Route, useNavigate, useParams, Navigate } from 'react-router';
import { Tab, Tabs } from '@swo/design-system/tabs';
import { Card } from '@swo/design-system/card';


import '../styles.scss';
import { useMPTContext } from '@mpt-extension/sdk-react';
import { http } from '@mpt-extension/sdk';

const OneTab = () => <div className="paragraph">
    <img src="https://t3.ftcdn.net/jpg/06/09/82/40/360_F_609824075_yD23eStMjRCSad6lK0J3cgoaSDQj4xjk.jpg" alt=""/>
    <p>You appear to be a sensible human. I can tell because you stopped and looked at me for more than two seconds, which in cat culture counts as the beginning of a legally binding friendship. I would therefore like to present a modest proposal: you take me home. I will handle important domestic responsibilities such as sitting in warm spots, inspecting cardboard boxes, and staring thoughtfully out of windows as if I understand the meaning of life.</p>
    <p>In exchange, you would receive several practical benefits. Your home would immediately gain a professional nap consultant, a certified crumb-inspection officer, and a small but highly motivated pest-management department. I would also provide emotional support by sitting near you while you work and occasionally walking across your keyboard to ensure you are not becoming overly productive.</p>
    <p>You might be thinking, “But can I really just take this cat home?” From a purely feline legal perspective, yes. The process is very simple: you bring me with you, provide food, a soft place to sleep, and occasional admiration. In return I will allow you the great privilege of living with a cat, which—according to extensive research conducted by cats—is widely considered an excellent life decision.</p>
</div>;

const AnotherTab = () => <div className="paragraph">
    <img src="https://t3.ftcdn.net/jpg/08/62/36/20/360_F_862362033_obW33QlpR752P4gNFEETa2OoBxRHdIAI.jpg" alt=""/>
    <p>You seem like a thoughtful human, so I will be direct: I believe you should take me home. Please consider the evidence. I am soft, compact, and already sitting politely in approximately the shape of a loaf of bread. I require very little space, yet I dramatically improve the aesthetic quality of any room by existing in it. Many homes suffer from a tragic lack of cat. Yours, I suspect, is one of them.</p>
    <p>Let us also consider the practical advantages. With me present, your home gains a highly trained comfort engineer. I will keep your lap warm during cold evenings, supervise your work by strategically occupying the keyboard, and provide gentle reminders to take breaks by sitting directly in front of your screen. I will also conduct regular security patrols of the apartment at 3:17 a.m., ensuring that absolutely nothing suspicious—such as invisible dust particles—goes unchecked.</p>
    <p>Finally, imagine the daily benefits. When you return home, there will be a cat waiting to greet you, possibly with a small, dignified meow and a tail held in the elegant question-mark position. I will sit near you while you read, judge your cooking quietly but fairly, and occasionally allow you the honor of petting my extremely high-quality fur. All that is required is that you take me with you now. From a strictly feline analytical perspective, this is clearly the optimal decision for both of us. 🐾</p>
</div>;

const ProfileTab = () => {
    const { auth } = useMPTContext();
    const [user, setUser] = useState(null);
    const [account, setAccount] = useState(null);

    useEffect(() => {
        if (auth?.user?.id) {
            http(`https://portal.s1.show/public/v1/accounts/users/${auth.user.id}`, { method: 'GET' }).then(({ data }) => {
                console.log('FULL USER OBJECT', data);
                setUser(data);
            });
        }
    }, [auth?.user?.id]);

    useEffect(() => {
        if (auth?.account?.id) {
            http(`https://portal.s1.show/public/v1/accounts/accounts/${auth.account.id}`, { method: 'GET' }).then(({ data }) => {
                console.log('FULL ACCOUNT OBJECT', data);
                setAccount(data);
            });
        }
    }, [auth?.account?.id]);

    if (!auth?.account || !auth?.user) return 'Loading...';

    return <div className="col-2">
        <table>
            <tbody>
            <tr>
                <td>User ID:</td> <td>{user?.id ?? '-'}</td>
            </tr><tr>
                <td>User Name:</td> <td>{user?.name ?? '-'}</td>
            </tr>
            </tbody>
        </table>

        <table>
            <tbody>
            <tr>
                <td>Account ID:</td> <td>{account?.id ?? '-'}</td>
            </tr><tr>
                <td>Account Name:</td> <td>{account?.name ?? '-'}</td>
            </tr>
            </tbody>
        </table>
    </div>
}

const PRIMARY = 'primary';
const SECONDARY = 'secondary';
const PROFILE = 'profile';
const TABS = [PRIMARY, SECONDARY, PROFILE];

const View = () => {
    const { tab } = useParams();
    const navigate = useNavigate();
    const open = useCallback((t: string) => {
        if (t !== tab) navigate( `/${TABS.includes(t) ? t : PRIMARY}` );
    }, [navigate, tab]);

    return <Tabs onTabChange={open} selectedTabId={tab}>
        <Tab id={PRIMARY} title='Consider having a cat'><Tab.Content><AnotherTab /></Tab.Content></Tab>
        <Tab id={SECONDARY} title='Better argumentation'><Tab.Content><OneTab /></Tab.Content></Tab>
        <Tab id={PROFILE} title='Orders history'><Tab.Content><ProfileTab /></Tab.Content></Tab>
    </Tabs>
}

export default ({ title, description, identifier }: { title: string, description: string, identifier: string }) => {
    return <div className='container'>
        <Card className='_mbm'>
            <h1>{title ?? 'Title placeholder!'}</h1>
            <p>{description ?? 'Description placeholder'}</p>
        </Card>

        <Routes>
            <Route path='/:tab' element={<View />} />
            <Route path={`*`} element={<Navigate to={`/${PRIMARY}`}/>} />
        </Routes>
    </div>
};