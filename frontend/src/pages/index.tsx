import React, { useEffect } from 'react';

import Analytics from '../components/Analytics';
import Canvas from '../components/Canvas';
import Features from '../components/Features';
import Header from '../components/Header';
import LazyShow from '../components/LazyShow';
import MainHero from '../components/MainHero';
import MainHeroImage from '../components/MainHeroImage';
import Product from '../components/Product';

import Dashboard from './dashboard';

const App = () => {
  const [isLogin, setIsLogin] = React.useState(false);

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (isLoggedIn) {
      setIsLogin(true);
    } 
  }, []);

  return (
    <>
      {!isLogin ? (
        <div className={`bg-background grid gap-y-16 overflow-hidden`}>
          <div className={`relative bg-background`}>
            <div className="max-w-7xl mx-auto">
              <div
                className={`relative z-10 pb-8 bg-background sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32`}
              >
                <Header />
                <MainHero  />
              </div>
            </div>
            <MainHeroImage />
          </div>
          <Canvas />
          <LazyShow>
            <>
              <Product />
              <Canvas />
            </>
          </LazyShow>
          <LazyShow>
            <Features />
          </LazyShow>
          <LazyShow>
            <Analytics />
          </LazyShow>
        </div>
      ) : (
            <Dashboard />
      )}
    </>
  );
};

export default App;
