import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="text-center">
                <h1 className="text-6xl font-bold text-gray-800 mb-4">404</h1>
                <p className="text-2xl text-gray-600 mb-8">Oops! The page you're looking for doesn't exist.</p>
                <Link to="/" className="text-blue-500 hover:text-blue-700 text-lg">
                    Go back to Home
                </Link>
            </div>
        </div>
    );
};

export default NotFound;
