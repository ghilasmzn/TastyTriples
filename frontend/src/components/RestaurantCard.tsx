import React, { useState } from "react";
import SearchService from "../services/SearchService";

interface RestaurantCardProps {
  id: string;
  image: string;
  name: string;
  description: string;
  telephone: string;
  price: string;
}

const RestaurantCard: React.FC<RestaurantCardProps> = ({
  id,
  image,
  name,
  description,
  telephone,
  price,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [restaurantDetails, setRestaurantDetails] = useState<any>({});
  const [showServiceDetails, setShowServiceDetails] = useState(false);

  const toggleServiceDetails = () => {
    setShowServiceDetails(!showServiceDetails);
  };

  const handleExpand = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    setIsExpanded(!isExpanded);

    if (!isExpanded) {
      const search = new SearchService();
      const results = await search.byId(id);
      setRestaurantDetails(results);
    }
  };

  return (
    <button
      className="relative bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition duration-500 cursor-pointer text-left"
      onClick={(e) => { e.preventDefault(); handleExpand(e); }}
    >
      <div className="flex items-center justify-between mb-2">
        <img className="h-10 w-10 rounded-full" src={image} alt="" />
        <button
          type="button"
          className="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium leading-5 bg-green-100 text-green-800"
        >
          {telephone}
        </button>
      </div>
      <p className="text-sm font-medium text-gray-900 truncate">{name}</p>
      <p className="text-sm text-gray-500 h-12 overflow-hidden">{description}</p>
      <div className="flex justify-end items-end">
        <div className="bg-gray-200 rounded-md py-1 px-3">
          <p className="text-sm text-gray-700 font-semibold">{price} €</p>
        </div>
      </div>

      {isExpanded && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-900 bg-opacity-50">
          <div className="flex items-center justify-center min-h-full px-4">
            <div className="bg-white rounded-lg max-w-4xl w-full p-8">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-3xl font-semibold">{restaurantDetails?.name}</h3>
                <button
                  onClick={() => setIsExpanded(false)}
                  className="text-gray-500 hover:text-gray-700 focus:outline-none"
                >
                  <svg
                    className="h-8 w-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M6 18L18 6M6 6l12 12"
                    ></path>
                  </svg>
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="mb-6 flex justify-center items-center">
                  <img
                    src={restaurantDetails?.image}
                    alt={restaurantDetails?.name}
                    className="w-full rounded-lg shadow-md h-full"
                  />
                </div>
                <div className="space-y-4 grid grid-cols-1">
                  <div>
                    <p className="text-gray-600 w-full">
                      {restaurantDetails?.description}
                    </p>
                  </div>
                  <div className="flex items-center">
                    <img src="/assets/images/address.svg" alt="address" className="inline-block w-6 h-6 mr-2" />
                    <p>{restaurantDetails?.streetAddress}</p>
                  </div>
                  <div className="flex items-center">
                    <img src="/assets/images/phone.svg" alt="phone" className="inline-block w-6 h-6 mr-2" />
                    <p>{restaurantDetails?.telephone}</p>
                  </div>
                  <div className="flex items-center flex-row">
                    <strong className="text-gray-600 mr-3">Price: </strong>
                    <div className="bg-gray-200 rounded-md py-1 px-3">
                      <p className="text-sm text-gray-700 font-semibold">{restaurantDetails?.price} €</p>
                    </div>
                  </div>
                  <div>
                    <strong className="text-gray-600">Opening Hours:</strong>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {restaurantDetails?.openingHours?.split(', ').map((dayHours: string, index: number) => (
                        <div key={index}>
                          <p>{dayHours}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                  <hr />
                </div>
              </div>

              <div className="space-y-4">
                {showServiceDetails && (
                  <>
                    <h3 className="text-3xl font-semibold">Service Details</h3>
                    <div>
                      <strong className="text-gray-600">Service Name:</strong>
                      <p>{restaurantDetails?.serviceName}</p>
                    </div>

                    <div>
                      <strong className="text-gray-600">Service Description:</strong>
                      <p>{restaurantDetails?.serviceDescription}</p>
                    </div>
                    <div>
                      <strong className="text-gray-600">Service Mail:</strong>
                      <p>{restaurantDetails?.serviceMail}</p>
                    </div>
                    <div>
                      <strong className="text-gray-600">Services Network:</strong>
                      <p>{restaurantDetails?.servicesNetwork}</p>
                    </div>
                  </>
                )}
              </div>
              <button
                onClick={(e) => { e.preventDefault(); e.stopPropagation(); toggleServiceDetails(); }}
                className="text-blue-500 hover:underline focus:outline-none w-full mt-5"
              >
                <span className="flex items-center justify-center text-center">
                  {showServiceDetails ? 'Read Less' : 'Read More'}
                </span>
              </button>
            </div>
          </div>
        </div>
      )}
    </button >
  );
};

export default RestaurantCard;
