import React from 'react';

interface TextInputProps {
  label: string;
  placeholder: string;
  name: string;
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const TextInput: React.FC<TextInputProps> = ({
  label,
  placeholder,
  name,
  value,
  onChange,
}) => {
  return (
    <div>
      <label
        htmlFor={name}
        className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
      >
        {label}
      </label>
      <input
        type="text"
        name={name}
        id={name}
        value={value}
        placeholder={placeholder}
        onChange={onChange}
        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:border-primary focus:outline-none dark:bg-gray-700 dark:text-gray-200"
      />
    </div>
  );
};

export default TextInput;