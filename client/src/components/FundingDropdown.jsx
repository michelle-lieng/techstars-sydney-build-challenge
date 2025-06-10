import { useState } from 'react'
import { fundingTags } from '../../utils/fundingTags'

export default function FundingTagsDropdown({ value, onChange }) {
    return (
        <div className="mb-3">
            <label htmlFor="search-funding" className="form-label">Funding Stage</label>
            <select
                className="form-select"
                id="search-funding"
                value={value}
                onChange={(e) => onChange(e.target.value)}
            >
                {fundingTags.map(fundingTag => (
                    fundingTag === "" ? (
                        <option value={fundingTag}>All Funding Stages</option>
                    ): (
                        
                        <option value={fundingTag}>{fundingTag}</option>
                )))} 
            </select>
        </div>
    );
}