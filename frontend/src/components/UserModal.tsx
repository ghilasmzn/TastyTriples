import React, { useState } from 'react';

const UserModal: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleModal = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="flex items-center">
      <div className="relative">
        <button
          type="button"
          className="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
          onClick={toggleModal}
          aria-expanded={isOpen ? 'true' : 'false'}
        >
          <span className="sr-only">Open user menu</span>
          <img
            className="w-8 h-8 rounded-full"
            src="assets/images/user-icon.png"
            alt="user icon"
          />
        </button>

        {isOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-800 bg-opacity-50">
            <div className="relative bg-white rounded-lg p-6 w-80 divide-y divide-gray-100 shadow-lg dark:bg-gray-700 dark:divide-gray-600">
              <button
                type="button"
                className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 focus:outline-none"
                onClick={toggleModal}
                aria-expanded={isOpen ? 'true' : 'false'}
              >
                <svg
                  className="w-5 h-5 fill-current"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                >
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" />
                </svg>
              </button>
              <div className="flex items-center mt-3">
                <div>
                  <img
                    className="w-8 h-8 rounded-full"
                    src="assets/images/user-icon.png"
                    alt="user icon"
                  />
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-900 dark:text-white">{localStorage.getItem('name')}</p>
                  <p className="text-sm font-medium text-gray-900 truncate dark:text-gray-300">
                    {localStorage.getItem('email')}
                  </p>
                </div>
              </div>
              <ul className="py-2">
                <li>
                  <a
                    href="#"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
                  >
                    Dashboard
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
                  >
                    Settings
                  </a>
                </li>
              </ul>
              <button
                onClick={() => {
                  localStorage.removeItem('isLoggedIn');
                  window.location.reload();
                }}
                className="ml-auto w-full mt-4 px-4 py-2 font-medium text-center text-red-600 bg-gray-100 rounded hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-red-500"
              >
                Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserModal;
