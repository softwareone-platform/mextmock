import { jsx as _jsx } from "react/jsx-runtime";
import Home from './pages/Home';
import About from './pages/About';
import './styles.scss';
import { createBrowserRouter, Outlet, RouterProvider } from 'react-router';
const layout = _jsx("div", { className: 'container', children: _jsx(Outlet, {}) });
export default () => {
    return _jsx("div", { children: _jsx(RouterProvider, { router: createBrowserRouter([
                {
                    path: "/",
                    element: layout,
                    children: [
                        { index: true, element: _jsx(Home, {}) },
                        { path: "about", element: _jsx(About, {}) }
                    ]
                }
            ]) }) });
};
