import Home from './pages/Home';
import About from './pages/About';

import './styles.scss';
import { createBrowserRouter, Outlet, RouterProvider } from 'react-router';

const layout = <div className='container'>
    <Outlet />
</div>;

export default () => {

    return <div>
        <RouterProvider router={createBrowserRouter([
            {
                path: "/",
                element: layout,
                children: [
                    { index: true, element: <Home /> },
                    { path: "about", element: <About /> }
                ]
            }
        ])} />
    </div>
};