import React, { useState, useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  isSignUpClicked: boolean;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, isSignUpClicked = true }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(isSignUpClicked);

  useEffect(() => {
    setIsSignUp(isSignUpClicked);
  }, [isSignUpClicked]);

  const handleSignUp = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Passwords don't match");
      return;
    }

    // TODO: Perform signup logic with email and password
    onClose();
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();

    // TODO: Perform login logic with email and password
    onClose();
  };

  return (
    isOpen && (
      <div className={`fixed inset-0 z-10 flex items-center justify-center backdrop-filter backdrop-blur-lg transition-opacity`}>
        <div className="relative bg-white p-8 rounded-lg w-full md:max-w-md">
          <div className="absolute top-0 right-0 m-6">
            <button
              onClick={onClose}
              className="relative top-2 right-2 text-gray-500 hover:text-gray-700 focus:outline-none"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
          <h2 className="text-3xl font-bold mb-6">{isSignUp ? 'Sign Up' : 'Login'}</h2>
          <form onSubmit={isSignUp ? handleSignUp : handleLogin}>
            <div className="mb-6">
              <label htmlFor="email" className="block mb-2">
                Email
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full border border-gray-300 rounded-md py-2 px-4 focus:border-primary focus:outline-none"
                required
              />

            </div>
            <div className="mb-6">
              <label htmlFor="password" className="block mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full border border-gray-300 rounded-md py-2 px-4 focus:border-primary focus:outline-none"
                required
              />
            </div>
            {isSignUp && (
              <div className="mb-6">
                <label htmlFor="confirmPassword" className="block mb-2">
                  Confirm Password
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full border border-gray-300 rounded-md py-2 px-4 focus:border-primary focus:outline-none"
                  required
                />
              </div>
            )}
            <button
              type="submit"
              className="w-full bg-primary text-white py-3 rounded-md hover:bg-opacity-80"
            >
              {isSignUp ? 'Sign Up' : 'Login'}
            </button>
          </form>
          <p className="mt-6 text-sm">
            {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
            <span
              className="text-primary cursor-pointer"
              onClick={() => setIsSignUp((prev) => !prev)}
            >
              {isSignUp ? 'Login here' : 'Sign Up here'}
            </span>
          </p>
        </div>
      </div>
    )
  );
};

export default Modal;
