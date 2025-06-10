import { useState } from 'react'
import { industryTags } from '../../utils/industryTags'

export default function IndustryTagsDropdown({ value, onChange }) {
    return (
        <div className="mb-3">
            <label htmlFor="search-industry" className="form-label">Industry</label>
            <select
                className="form-select"
                id="search-industry"
                value={value}
                onChange={(e) => onChange(e.target.value)}
            >
                {industryTags.map(industryTag => (
                    industryTag === "" ? (
                        <option value={industryTag}>All Industries</option>
                    ): (
                        
                        <option value={industryTag}>{industryTag}</option>
                )))} 
            </select>
        </div>
    );
}