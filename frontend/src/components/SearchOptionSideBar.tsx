import React, { useState } from 'react';

import LogInHeader from './LogInHeader';

const SearchOptionsSidebar: React.FC = () => {

  const [rangeValue, setRangeValue] = useState(50);

  const handleRangeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRangeValue(Number(event.target.value));
  };


  return (
    <>
      <LogInHeader />
      <aside
        id="logo-sidebar"
        className="fixed top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform -translate-x-full bg-white border-r border-gray-200 sm:translate-x-0 dark:bg-gray-800 dark:border-gray-700"
        aria-label="Sidebar"
      >
        <div className="h-full px-3 pb-4 overflow-y-auto bg-white dark:bg-gray-800">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Search Options
          </h2>
          <div className="space-y-4">
            {/* Filter: Location */}
            <div>
              <label
                htmlFor="location"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Location
              </label>
              <input
                type="text"
                id="location"
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:border-primary focus:outline-none dark:bg-gray-700 dark:text-gray-200"
                placeholder="Enter location"
              />
            </div>

              {/* Filter: Distance range with slider input */}
              <div>
                <label htmlFor="default-range" className="block space-y-4 mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  Search range
                </label>
                <div className="flex items-center justify-center space-x-4">
                  <input
                    id="default-range"
                    type="range"
                    value={rangeValue}
                    min={0}
                    max={150}
                    step={1}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
                    onChange={handleRangeChange}
                  />
                  <span className="text-gray-700 dark:text-gray-300">{rangeValue}</span>
                </div>
            </div>

            {/* Filter: Cuisine */}
            <div>
              <label
                htmlFor="cuisine"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Cuisine
              </label>
              <select
                id="cuisine"
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:border-primary focus:outline-none dark:bg-gray-700 dark:text-gray-200"
              >
                <option value="">Select cuisine</option>
                <option value="italian">Italian</option>
                <option value="indian">Indian</option>
              </select>
            </div>

            {/* Filter: Rating */}
            <div>
              <label
                htmlFor="rating"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Minimum Rating
              </label>
              <input
                type="number"
                id="rating"
                min="1"
                max="5"
                step="0.5"
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:border-primary focus:outline-none dark:bg-gray-700 dark:text-gray-200"
                placeholder="Enter minimum rating"
              />
            </div>

            {/* Filter: Price Range */}
            <div>
              <label
                htmlFor="priceRange"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >
                Price Range
              </label>
              <input
                type="text"
                id="priceRange"
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:border-primary focus:outline-none dark:bg-gray-700 dark:text-gray-200"
                placeholder="Enter price range"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="openNow"
                className="h-4 w-4 rounded border-gray-300 focus:ring focus:border-blue-300 dark:bg-gray-700 dark:text-gray-200"
              />
              <label
                htmlFor="openNow"
                className="ml-2 text-sm font-medium text-gray-700 dark:text-gray-300"
              >
                Open Now
              </label>
            </div>

            <button
              className="w-full bg-secondary text-white font-semibold py-2 px-4 rounded-md hover:bg-primary focus:outline-none focus:bg-primary"
              type="button"
            >
              Apply Filters
            </button>
          </div>
        </div>
      </aside>
    </>
  );
};

export default SearchOptionsSidebar;