import React, { useState } from 'react';
import SearchOptionsSidebar from '../components/SearchOptionSideBar';

import RestaurantCard from '../components/RestaurantCard';
import SearchInput from '../components/SearchInput';


const DashboardComponent: React.FC = () => {

  const [results, setResults] = useState<any[]>([]);

  return (
    <div className="flex bg-gray-100 min-h-screen">
      <div className="hidden md:block w-64">
        <SearchOptionsSidebar setResults={setResults} />
      </div>

      {results.length === 0 ? (
          <SearchInput setResults={setResults} />
      ) : (
        <div className="flex-grow flex flex-col items-center w-2/3">
          <div className="w-full p-6">
            <div className="flex items-center mb-4 mt-12">
              <button
                onClick={() => setResults([])}
                className="flex items-center bg-transparent text-red-700 font-bold py-2 px-4 rounded focus:outline-none"
                type="button"
              >
                <svg
                  className="w-6 h-6 mr-2 hover:text-red-900"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
              </button>

              <h2 className="text-3xl font-semibold text-center text-primary">
                Search Results ({results.length})
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((result: any) => (
                <RestaurantCard
                  key={result.restaurant}
                  id={result.restaurant}
                  name={result.name}
                  description={result.description}
                  image={result.image}
                  telephone={result.telephone}
                  price={result.price}
                />
              ))}
            </div>
          </div>
        </div >
      )}
    </div>
  );
};

export default DashboardComponent;
