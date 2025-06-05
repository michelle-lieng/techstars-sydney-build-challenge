import { useState } from 'react'
import { tags } from '../../utils/tagsList'

export default function TagsDropdown({ value, onChange }) {
    const handleCheckboxChange = (tag) => {
        if (value.includes(tag)) {
            onChange(value.filter(t => t !== tag));
        } else {
            onChange([...value, tag]);
        }
    };

    return (
        <div className="tags-container" id="tags-container">
            {tags.map(tag => (
            <div key={tag} className="form-check">
                <input
                    className="form-check-input"
                    type="checkbox"
                    value={tag}
                    id={`tag-${tag.replace(/\s+/g, '-').toLowerCase()}`}
                    checked={value.includes(tag)}
                    onChange={() => handleCheckboxChange(tag)}
                />
                <label className="form-check-label" htmlFor={`tag-${tag.replace(/\s+/g, '-').toLowerCase()}`}>
                {tag}
                </label>
            </div>
            ))}
        </div>
    )
}