import { useState } from 'react'
import { personaTags } from '../../utils/personaTags'

export default function PersonaTagsDropdown({ value, onChange }) {
    return (
        <div className="mb-3">
            <label htmlFor="search-persona" className="form-label">Persona</label>
            <select
                className="form-select"
                id="search-persona"
                value={value}
                onChange={(e) => onChange(e.target.value)}
            >
                {personaTags.map(personaTag => (
                    personaTag === "" ? (
                        <option value={personaTag}>All Personas</option>
                    ): (
                        
                        <option value={personaTag}>{personaTag}</option>
                )))} 
            </select>
        </div>
    );
}