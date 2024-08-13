import React from 'react';
import Navbar from './Navbar'; // Make sure the path is correct for your project

const Layout = ({ children }) => {
    return (
        <div>
            <Navbar />
            <div>{children}</div>
        </div>
    );
};

export default Layout;
