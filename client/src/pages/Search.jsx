import React, { useState, useEffect } from 'react'
import FounderCard  from '../components/FounderCard';

export default function Search() {
    const handleSubmit = (e) => {
        e.preventDefault();
    
        const params = new URLSearchParams();
    
        if (nameFilter) params.append('name', nameFilter);
        if (cityFilter) params.append('city', cityFilter);
        if (startupFilter) params.append('startup', startupFilter);
        if (genderFilter) params.append('gender', genderFilter);
        if (ethnicityFilter) params.append('ethnicity', ethnicityFilter);
        if (migrantFilter) params.append('migrant', migrantFilter);
    
        fetch(`/api/search?${params.toString()}`)
            .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
            })
            .then((data) => {
            setFounders(data);
            setLoading(false);
            })
            .catch((error) => {
            console.error('Error fetching data:', error);
            setError(error);
            setLoading(false);
        });

        resetFilters()
    };  
    
    const resetFilters = () => {
        setNameFilter('');
        setCityFilter('');
        setStartupFilter('');
        setGenderFilter('');
        setEthnicityFilter('');
        setMigrantFilter('');
        
        fetch('/api/search')
            .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
            })
            .then((data) => {
            setFounders(data);
            setLoading(false);
            })
            .catch((error) => {
            console.error('Error fetching data:', error);
            setError(error);
            setLoading(false);
        });
    };

    const [founders, setFounders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [nameFilter, setNameFilter] = useState('');
    const [cityFilter, setCityFilter] = useState('');
    const [startupFilter, setStartupFilter] = useState('');
    const [genderFilter, setGenderFilter] = useState('');
    const [ethnicityFilter, setEthnicityFilter] = useState('');
    const [migrantFilter, setMigrantFilter] = useState('');

    useEffect(() => {
        fetch('api/search')
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                setFounders(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
                setError(error);
                setLoading(false);
            })
    }, []);
    return (
        <main>
            <div className="container mt-4">
                <div className="row">
                    <div className="col-12">
                        <h1>Search Hidden Founders</h1>
                        <p className="lead">Find high-potential founders across Australia using advanced filters.</p>
                    </div>
                </div>

                <div className="row mt-3">
                    <div className="col-md-3">
                        <div className="card shadow-sm mb-4">
                            <div className="card-header bg-light">
                                <h5 className="card-title mb-0">Filters</h5>
                            </div>
                            <div className="card-body">
                                <form id="search-form" onSubmit={handleSubmit}>
                                    <div className="mb-3">
                                        <label htmlFor="search-name" className="form-label">Name</label>
                                        <input type="text" className="form-control" id="search-name" placeholder="Enter name" value={nameFilter} onChange={(e) => setNameFilter(e.target.value)}/>
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="search-city" className="form-label">City</label>
                                        <select className="form-select" id="search-city" value={cityFilter} onChange={(e) => setCityFilter(e.target.value)}>
                                        </select>
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="search-startup" className="form-label">Startup Name</label>
                                        <input type="text" className="form-control" id="search-startup" placeholder="Enter startup name" value={startupFilter} onChange={(e) => setStartupFilter(e.target.value)}/>
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label className="form-label">Founder Type</label>
                                        <div className="tags-container" id="tags-container">
                                            {/* {tags.map(tag => (
                                            <div key={tag.id} className="form-check">
                                                <input
                                                className="form-check-input"
                                                type="checkbox"
                                                value={tag.name}
                                                id={`tag-${tag.id}`}
                                                />
                                                <label className="form-check-label" htmlFor={`tag-${tag.id}`}>
                                                {tag.name}
                                                </label>
                                            </div>
                                            ))} */}
                                        </div>
                                    </div>
                                    
                                    <hr/>
                                    
                                    <h6 className="mb-3">Diversity Filters</h6>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="search-gender" className="form-label">Gender</label>
                                        <select className="form-select" id="search-gender" value={genderFilter} onChange={(e) => setGenderFilter(e.target.value)}>
                                            <option value="">All Genders</option>
                                            <option value="Female">Female</option>
                                            <option value="Male">Male</option>
                                            <option value="Non-binary">Non-binary</option>
                                        </select>
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="search-ethnicity" className="form-label">Ethnicity</label>
                                        <select className="form-select" id="search-ethnicity" value={ethnicityFilter} onChange={(e) => setEthnicityFilter(e.target.value)}>
                                            <option value="">All Ethnicities</option>
                                            <option value="European Australian">European Australian</option>
                                            <option value="Asian Australian">Asian Australian</option>
                                            <option value="Indigenous Australian">Indigenous Australian</option>
                                            <option value="Middle Eastern Australian">Middle Eastern Australian</option>
                                            <option value="African Australian">African Australian</option>
                                            <option value="Pacific Islander Australian">Pacific Islander Australian</option>
                                            <option value="South Asian Australian">South Asian Australian</option>
                                            <option value="Mixed Heritage">Mixed Heritage</option>
                                        </select>
                                    </div>
                                    
                                    <div className="mb-3">
                                        <label htmlFor="search-migrant" className="form-label">Migrant Status</label>
                                        <select className="form-select" id="search-migrant" value={migrantFilter} onChange={(e) => setMigrantFilter(e.target.value)}>
                                            <option value="">All</option>
                                            <option value="true">Migrant Founders</option>
                                            <option value="false">Non-Migrant Founders</option>
                                        </select>
                                    </div>
                                    
                                    <div className="d-grid">
                                        <button type="submit" className="btn btn-primary">Apply Filters</button>
                                        <button type="button" className="btn btn-outline-secondary mt-2" id="reset-filters" onClick={resetFilters}>
                                            Reset Filters
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    
                    <div className="col-md-9">
                        <div className="card shadow-sm mb-4">
                            <div className="card-header bg-light d-flex justify-content-between align-items-center">
                                <h5 className="card-title mb-0">Results <span id="result-count" className="badge bg-primary ms-2">0</span></h5>
                                <div className="d-flex align-items-center">
                                    <label htmlFor="sort-by" className="form-label me-2 mb-0">Sort by:</label>
                                    <select className="form-select form-select-sm" id="sort-by" style={{ width: 'auto' }}>
                                        <option value="profile_completeness">Completeness</option>
                                        <option value="name">Name</option>
                                        <option value="city">City</option>
                                    </select>
                                </div>
                            </div>
                            <div className="card-body">
                                { loading ? (
                                    <div id="search-results" className="row">
                                        <div className="col-12 text-center py-5">
                                            <div className="spinner-border text-primary" role="status">
                                                <span className="visually-hidden">Loading...</span>
                                            </div>
                                            <p className="mt-3">Loading founders...</p>
                                        </div>
                                    </div>

                                ) : error ? (
                                    <div className="alert alert-danger" role="alert">
                                        Error fetching data: {error.message}
                                    </div>                                  
                                ): founders.length === 0 ? ( 
                                    <div className="alert alert-warning" role="alert">
                                        No founders found.
                                    </div>                                    
                                ) : (
                                    <div className="row" id="search-results">
                                        {founders.map((founder) => (
                                        <FounderCard key={founder.id} founder={founder} />
                                        ))}
                                    </div>                                   
                                )}
                                
                                <div id="pagination" className="d-flex justify-content-center mt-4">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>            
        </main>
    )
}