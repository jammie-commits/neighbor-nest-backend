import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="bg-blue-600 p-4">
            <div className="container mx-auto flex items-center justify-between">
                <div className="text-white text-2xl font-bold">
                    <Link to="/">NeighborNest</Link>
                </div>
                <div className="hidden md:flex space-x-4">
                    <Link to="/" className="text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium">
                        Home
                    </Link>
                    <Link to="/events" className="text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium">
                        Events
                    </Link>
                    <Link to="/dashboard" className="text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium">
                        Dashboard
                    </Link>
                    <Link to="/profile" className="text-white hover:bg-blue-700 px-3 py-2 rounded-md text-sm font-medium">
                        Profile
                    </Link>
                </div>
                <div className="md:hidden flex items-center">
                    <button className="text-white focus:outline-none">
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
