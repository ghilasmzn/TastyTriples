import React, { useEffect, useState } from 'react';

import LogInHeader from './LogInHeader';
import Select from 'react-select';

import TextInput from './input/TextInput';

import SearchService from '../services/SearchService';
import SliderInput from './input/SliderInput';

interface SearchOptionsSidebarProps {
  setResults: (results: any[]) => void;
}

const SearchOptionsSidebar: React.FC<SearchOptionsSidebarProps> = ({ setResults }) => {
  const [rangeValue, setRangeValue] = useState(50);

  const [geoLocation, setGeoLocation] = useState<number[]>([]);
  const [location, setLocation] = useState<string>("");

  const [suggestedCommunes, setSuggestedCommunes] = useState<any[]>([]);
  const [isLocationInputFocused, setIsLocationInputFocused] = useState(false);

  const [selectedDays, setSelectedDays] = useState<any[]>([]);

  const [minPrice, setMinPrice] = useState<number>(0);
  const [maxPrice, setMaxPrice] = useState<number>(0);

  const [sortByDeliveryPrice, setSortByDeliveryPrice] = useState(false);

  const days = [
    { label: "Monday", value: "Monday" },
    { label: "Tuesday", value: "Tuesday" },
    { label: "Wednesday", value: "Wednesday" },
    { label: "Thursday", value: "Thursday" },
    { label: "Friday", value: "Friday" },
    { label: "Saturday", value: "Saturday" },
    { label: "Sunday", value: "Sunday" },
  ];

  const handleSelectedDays = (selectedDays: any) => {
    setSelectedDays(selectedDays);
  };

  const handleRangeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRangeValue(Number(event.target.value));
  };

  const handleMinPriceChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMinPrice(Number(event.target.value));
  };

  const handleMaxPriceChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMaxPrice(Number(event.target.value));
  };

  const handleDeliveryPriceToggle = () => {
    setSortByDeliveryPrice((prevSort) => !prevSort);
  };

  const handleFocus = () => {
    setIsLocationInputFocused(true);
  };

  const handleBlur = () => {
    setTimeout(() => {
      setIsLocationInputFocused(false);
    }, 100);
  }

  const fetchCommuneSuggestions = async (searchQuery: string) => {
    try {
      const response = await fetch(`https://api-adresse.data.gouv.fr/search/?q=${searchQuery}&type=municipality&autocomplete=1`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }
      const data = await response.json();
      setSuggestedCommunes(data.features);
    } catch (error) {
      console.warn("Error fetching commune suggestions: ", error);
      setSuggestedCommunes([]);
    }
  };

  const onSearch = async () => {
    const search = new SearchService();

    const days: string[] = selectedDays.map(day => day.label);
    const results = await search.withFilters(location, geoLocation, location ? rangeValue : 0, days, minPrice, maxPrice, sortByDeliveryPrice);
    setResults(results ?? []);
  }

  const handleSelectCommune = (selectedCommune: any) => {
    setLocation(selectedCommune.properties.city);
    setGeoLocation(selectedCommune.geometry.coordinates);
  };

  useEffect(() => {
    if (location.trim() !== "") {
      fetchCommuneSuggestions(location);
    } else {
      setSuggestedCommunes([]);
    }
  }, [location]);


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
            <div className="relative">
              <TextInput
                label="Location"
                name="location"
                value={location}
                placeholder="Enter location"
                onChange={(event) => setLocation(event.target.value)}
                onBlur={handleBlur}
                onFocus={handleFocus}
              />

              {isLocationInputFocused && suggestedCommunes.length > 0 && (
                <ul className="absolute top-full left-0 w-full bg-white shadow-md py-2 mt-1 rounded-md border border-gray-300 z-50">
                  {suggestedCommunes.map((commune) => (
                    <li key={commune.properties.id} className="px-4 py-2 hover:bg-gray-100 cursor-pointer">
                      <button onClick={() => handleSelectCommune(commune)} className="w-full text-left focus:outline-none">
                        <div>
                          <p className="font-semibold mb-1">{commune.properties.municipality}</p>
                          <p className="text-sm text-gray-600">{commune.properties.context}</p>
                        </div>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {/* Filter: Distance range with slider input */}
            {location && (
              <SliderInput
                label="Distance"
                name="distance"
                value={rangeValue}
                onChange={handleRangeChange}
              />
            )}

            {/* Filter: Price Range */}
            <div className="flex space-x-4">
              <div>
                <TextInput
                  label="Min Price"
                  placeholder="Enter minimum price"
                  name="minPrice"
                  value={minPrice}
                  onChange={handleMinPriceChange}
                />
              </div>

              <div>
                <TextInput
                  label="Max Price"
                  placeholder="Enter maximum price"
                  name="maxPrice"
                  value={maxPrice}
                  onChange={handleMaxPriceChange}
                />
              </div>
            </div>

            {/* Filter: Days */}
            <div className="mb-4">
              <div className="flex flex-wrap">
                <label htmlFor="days" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Select Days
                </label>
                <Select
                  isMulti
                  name="colors"
                  options={days}
                  className="basic-multi-select w-full"
                  classNamePrefix="select"
                  onChange={handleSelectedDays}
                />
              </div>
            </div>


            {/* Sort by: delivery price (asc or desc) */}
            <div className="flex items-center justify-between">
              <label htmlFor="deliveryPrice" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Sort by Delivery Price
              </label>

              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" value="" className="sr-only peer" onChange={handleDeliveryPriceToggle} />
                <div
                  className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[#ff637088] dark:peer-focus:ring-[#a12c34] rounded-full peer dark:bg-[#99a0a3] peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-[#ec4755]"
                >
                </div>
              </label>
            </div>

            <button
              onClick={onSearch}
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