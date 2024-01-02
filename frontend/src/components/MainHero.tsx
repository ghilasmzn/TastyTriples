import { useState } from 'react';

import Modal from './Modal';
import config from '../config/index.json';

const MainHero = () => {
  const { mainHero } = config;
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSignUpClicked, setIsSignUpClicked] = useState(false);

  const openModal = (buttonText: string) => {
    setIsModalOpen(true);
    setIsSignUpClicked(buttonText === mainHero.secondaryAction.text);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
      <div className="sm:text-center lg:text-left">
        <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
          <span className="block xl:inline">{mainHero.title}</span>{' '}
          <span className={`block text-primary xl:inline`}>
            {mainHero.subtitle}
          </span>
        </h1>
        <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
          {mainHero.description}
        </p>
        <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
          <div className="rounded-md shadow">
            <button
              onClick={() => openModal(mainHero.primaryAction.text)}
              className={`w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-background bg-primary hover:bg-border hover:text-primary md:py-4 md:text-lg md:px-10`}
            >
              {mainHero.primaryAction.text}
            </button>
          </div>
          <div className="mt-3 sm:mt-0 sm:ml-3">
            <button
              onClick={() => openModal(mainHero.secondaryAction.text)}
              className={`w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md border-primary text-secondary bg-background hover:bg-border hover:text-primary md:py-4 md:text-lg md:px-10`}
            >
              {mainHero.secondaryAction.text}
            </button>
          </div>
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={closeModal} isSignUpClicked={isSignUpClicked} />
    </main>
  );
};

export default MainHero;
