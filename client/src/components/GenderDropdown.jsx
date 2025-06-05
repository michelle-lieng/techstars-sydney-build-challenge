import React, { useState } from 'react';

export default function GenderDropdown({ value, onChange }) {
  return (
    <div className="mb-3">
      <label htmlFor="search-gender" className="form-label">Gender</label>
      <select
        className="form-select"
        id="search-gender"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">All Genders</option>
        <option value="Female">Female</option>
        <option value="Male">Male</option>
        <option value="Non-binary">Non-binary</option>
      </select>
    </div>
  );
}