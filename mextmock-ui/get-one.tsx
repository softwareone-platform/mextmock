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
              title="Please consider having a cat"
              description="You can find some reasonable arguments below."
              identifier='get-one'
            />
        </BrowserRouter>
    );
});