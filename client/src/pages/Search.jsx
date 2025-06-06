import React, { useState, useEffect } from 'react'
import FounderCard  from '../components/FounderCard';
import GenderDropdown from '../components/GenderDropdown';
import TagsDropdown from '../components/Tags';
import MigrantDropdown from '../components/Migrant';
import Pagination from '../components/Pagination';
import { 
    initTooltips,
    initPopovers,
    makeTablesResponsive,
    setupScrollAnimation
 } from '../../utils/helper';

export default function Search() {
    const [debouncedNameFilter, setDebouncedNameFilter] = useState('');
    const [debouncedStartupFilter, setDebouncedStartupFilter] = useState('');
    const [founders, setFounders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [nameFilter, setNameFilter] = useState('');
    const [cityFilter, setCityFilter] = useState('');
    const [startupFilter, setStartupFilter] = useState('');
    const [genderFilter, setGenderFilter] = useState('');
    const [migrantFilter, setMigrantFilter] = useState('');
    const [tagsFilter, setTagsFilter] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const foundersPerPage = 10;

    const indexOfLastFounder = currentPage * foundersPerPage;
    const indexOfFirstFounder = indexOfLastFounder - foundersPerPage;
    const currentFounders = founders.slice(indexOfFirstFounder, indexOfLastFounder);

    const totalPages = Math.ceil(founders.length / foundersPerPage);
    
    const resetFilters = () => {
        setNameFilter('');
        setCityFilter('');
        setStartupFilter('');
        setGenderFilter('');
        setMigrantFilter('');
        setTagsFilter([]);
    };


    useEffect(() => {
        const params = new URLSearchParams();
    
        if (nameFilter) params.append('name', nameFilter);
        if (cityFilter) params.append('city', cityFilter);
        if (startupFilter) params.append('startup', startupFilter);
        if (genderFilter) params.append('gender', genderFilter);
        if (migrantFilter) params.append('migrant', migrantFilter);
        
        if (tagsFilter.length > 0) {
            tagsFilter.forEach(tag => params.append('tags', tag)); 
        }
        
        setLoading(true);

        fetch(`/api/search?${params.toString()}`)
            .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
            })
            .then((data) => {
            setFounders(data);
            setCurrentPage(1);
            setLoading(false);
            })
            .catch((error) => {
            console.error('Error fetching data:', error);
            setError(error);
            setLoading(false);
        });
    }, [nameFilter, cityFilter, startupFilter, genderFilter, migrantFilter, tagsFilter]);

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedNameFilter(nameFilter);
            setDebouncedStartupFilter(startupFilter);
        }, 5000);
        
        return () => clearTimeout(timer);
    }, [nameFilter, startupFilter]);

    useEffect(() => {
    if (!loading && founders.length > 0) {
        initTooltips();
        initPopovers();
        makeTablesResponsive();
        setupScrollAnimation();
    }
    }, [loading, founders]);

    useEffect(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, [currentPage]);
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
                                <form id="search-form" onSubmit={(e) => e.preventDefault()}>
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
                                        <label className="form-label">Tags</label>
                                        <TagsDropdown
                                            value={tagsFilter}
                                            onChange={setTagsFilter}
                                        />
                                    </div>
                                    
                                    <hr/>
                                    
                                    <h6 className="mb-3">Diversity Filters</h6>
                                    
                                    <GenderDropdown
                                        value={genderFilter}
                                        onChange={setGenderFilter}
                                    />
                                
                                    <div className="mb-3">
                                        <label htmlFor="search-migrant" className="form-label">Migrant Status</label>
                                        <MigrantDropdown 
                                            value={migrantFilter}
                                            onChange={setMigrantFilter}    
                                        />
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
                                <h5 className="card-title mb-0">Results <span id="result-count" className="badge bg-primary ms-2">{ founders.length }</span></h5>
                                <div className="d-flex align-items-center">
                                    <label htmlFor="sort-by" className="form-label me-2 mb-0">Sort by:</label>
                                    <select className="form-select form-select-sm" id="sort-by" style={{ width: 'auto' }}>
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
                                        {currentFounders.map((founder) => (
                                        <FounderCard key={founder.id} founder={founder} />
                                        ))}
                                    </div>                                   
                                )}
                                
                                <div id="pagination" className="d-flex justify-content-center mt-4">
                                    {totalPages > 1 && (
                                        <Pagination
                                            currentPage={currentPage}
                                            totalPages={totalPages}
                                            setCurrentPage={setCurrentPage}
                                        />
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>            
        </main>
    )
}