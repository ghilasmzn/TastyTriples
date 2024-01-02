import React from 'react';
import SearchOptionsSidebar from '../components/SearchOptionSideBar';

const DashboardComponent: React.FC = () => {
  return (
    <div className="flex bg-gray-100 min-h-screen">
      <div className="hidden md:block md:w-1/4 lg:w-1/5">
        <SearchOptionsSidebar />
      </div>

      <div className="flex-grow flex flex-col items-center justify-center">
        <div className="w-2/3">
          <h2 className="text-3xl font-semibold text-center mb-8 text-primary">
            Search for Restaurants
          </h2>

          <div className="mb-4">
            <input
              className="shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="keyword"
              type="text"
              placeholder="Enter keywords..."
            />
          </div>

          <div className="text-center">
            <button
              className="bg-red-700 hover:bg-red-900 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
            >
              Search
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardComponent;
