import React from "react";

import SearchService from "../services/SearchService";

interface SearchInputProps {
  setResults: any;
}

const SearchInput: React.FC<SearchInputProps> = ({ setResults }) => {

  const search = async () => {
    const keywords = (document.getElementById('keyword') as HTMLInputElement).value;

    const searchService = new SearchService();
    const results = await searchService.searchRestaurants(keywords);
    console.log(results?.length);

    setResults(results ?? []);
  }

  return (
    <div className="flex-grow flex flex-col items-center justify-center w-2/3">
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
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                search();
              }
            }}
          />
        </div>

        <div className="text-center">
          <button
            onClick={search}
            className="bg-red-700 hover:bg-red-900 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
          >
            Search
          </button>
        </div>
      </div>
    </div>
  )
}

export default SearchInput;