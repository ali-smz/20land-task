// components/MobileInput.jsx
import React from "react";

const MobileInput = ({ value, onChange }) => {
  return (
    <div className="mb-4">
      <label className="block mb-2 text-gray-700 font-semibold">
        شماره موبایل:
      </label>
      <input
        type="tel"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="مثال: 09123456789"
        className="w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
    </div>
  );
};

export default MobileInput;
