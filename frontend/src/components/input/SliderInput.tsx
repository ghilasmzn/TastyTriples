import React from 'react';

interface SliderInputProps {
  label: string;
  name: string;
  value: number;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const SliderInput: React.FC<SliderInputProps> = ({
  label,
  name,
  value,
  onChange,
}) => {
  return (
    <div>
      <label htmlFor={name} className="block space-y-4 mb-2 text-sm font-medium text-gray-900 dark:text-white">
        {label}
      </label>
      <div className="flex items-center justify-center space-x-4">
        <input
          id={name}
          type="range"
          value={value}
          min={0}
          max={150}
          step={1}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
          onChange={onChange}
        />
        <span className="text-gray-700 dark:text-gray-300">{value}</span>
      </div>
    </div>
  );
};

export default SliderInput;