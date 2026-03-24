import React from 'react';
import { createRoot } from 'react-dom/client';
import { setup } from '@mpt-extension/sdk';
import { BrowserRouter } from "react-router";

import App from './page/App';

setup((element: Element) => {
    const root = createRoot(element);
    root.render(
        <BrowserRouter>
            <App
              title="Donations history"
              description="Check out previous donations before making more generous one."
              identifier='history'
            />
        </BrowserRouter>
    );
});