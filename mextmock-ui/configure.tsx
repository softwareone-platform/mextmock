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
              title="Configure your donation."
              description="Make a generous donation for a cute cat."
              identifier='configure'
            />
        </BrowserRouter>
    );
});