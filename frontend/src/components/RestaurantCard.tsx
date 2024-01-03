import React from "react";

interface RestaurantCardProps {
  image: string;
  name: string;
  description: string;
  telephone: string;
  price: string;
}

const RestaurantCard: React.FC<RestaurantCardProps> = ({ image, name, description, telephone, price }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 relative">
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
    </div>
  );
};

export default RestaurantCard;
