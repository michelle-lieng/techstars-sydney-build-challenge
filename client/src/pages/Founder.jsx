import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

export default function FounderProfile() {
    // Extract founderId from URL parameters
    const { founderId } = useParams();
    const [founderData, setFounderData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
    const fetchFounderData = async () => {
        try {
        setLoading(true);
        setError(null);
        
        // Replace with your actual API endpoint
        const response = await fetch(`/api/founders/${founderId}`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch founder data: ${response.status}`);
        }
        
        const data = await response.json();
        setFounderData(data);
        setLoading(false);
        } catch (err) {
        console.error('Error fetching founder data:', err);
        setError(err.message);
        setLoading(false);
        }
    };

    if (founderId) {
        fetchFounderData();
    }
    }, [founderId]);

    // Helper function to check if a value exists and is not empty
    const hasValue = (value) => {
    if (value === null || value === undefined) return false;
    if (typeof value === 'string') return value.trim() !== '';
    if (Array.isArray(value)) return value.length > 0;
    return true;
    };

    // Format date from YYYY-MM-DD to Month Year
    const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
    };

    // Show loading spinner while data is being fetched
    if (loading) {
    return (
        <div className="row mt-3">
        <div className="col-12 text-center py-5">
            <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3">Loading founder profile...</p>
        </div>
        </div>
    );
    }

    // Show error message if fetch failed
    if (error) {
    return (
        <div className="row mt-3">
        <div className="col-12 text-center py-5">
            <div className="alert alert-danger" role="alert">
            <i className="bi bi-exclamation-triangle me-2"></i>
            {error}
            </div>
            <button 
            className="btn btn-primary mt-3" 
            onClick={() => window.location.reload()}
            >
            Try Again
            </button>
        </div>
        </div>
    );
    }

    // Show message if no data was found
    if (!founderData) {
    return (
        <div className="row mt-3">
        <div className="col-12 text-center py-5">
            <div className="alert alert-warning" role="alert">
            <i className="bi bi-info-circle me-2"></i>
            No founder data found for ID: {founderId}
            </div>
        </div>
        </div>
    );
    }

    return (
        <div className="container">
            <div id="profile-content" className="row mt-3">
            <div className="col-md-4">
                {/* Profile Card */}
                <div className="card shadow-sm mb-4">
                <div className="card-body">
                    <div className="text-center mb-3">
                    <div className="profile-image-placeholder rounded-circle mx-auto mb-3">
                        <i className="bi bi-person-fill"></i>
                    </div>
                    {hasValue(founderData.name) && (
                        <h2 className="mb-0">{founderData.name}</h2>
                    )}
                    {hasValue(founderData.city) && (
                        <p className="text-muted">
                        <i className="bi bi-geo-alt"></i> <span>{founderData.city}</span>
                        </p>
                    )}
                    </div>
                    
                    {/* Current Role */}
                    {(hasValue(founderData.current_title) || hasValue(founderData.current_company)) && (
                    <div className="mb-3">
                        <h6 className="text-uppercase text-muted small">Current Role</h6>
                        <p className="mb-0">
                        {hasValue(founderData.current_title) && founderData.current_title}
                        {hasValue(founderData.current_title) && hasValue(founderData.current_company) && ' at '}
                        {hasValue(founderData.current_company) && founderData.current_company}
                        {hasValue(founderData.current_job_start) && (
                            <span className="text-muted d-block small">
                            Since {formatDate(founderData.current_job_start)}
                            </span>
                        )}
                        </p>
                    </div>
                    )}
                    
                    {/* Current Startup - Only show if is_current_founder is true */}
                    {founderData.is_current_founder === 1 && (
                    <div className="mb-3">
                        <h6 className="text-uppercase text-muted small">Startup</h6>
                        <p className="mb-0">
                        {hasValue(founderData.current_company) && (
                            <strong>{founderData.current_company}</strong>
                        )}
                        {hasValue(founderData.curr_startup_funding_stage) && (
                            <span className="d-block small">
                            {founderData.curr_startup_funding_stage} stage
                            </span>
                        )}
                        {hasValue(founderData.curr_startup_url) && (
                            <a 
                            href={founderData.curr_startup_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="d-block small text-truncate"
                            >
                            {founderData.curr_startup_url}
                            </a>
                        )}
                        {hasValue(founderData.curr_startup_info) && (
                            <span className="d-block mt-2">{founderData.curr_startup_info}</span>
                        )}
                        </p>
                    </div>
                    )}
                    
                    {/* Industry Focus */}
                    {hasValue(founderData.curr_startup_industry) && (
                    <div className="mb-3">
                        <h6 className="text-uppercase text-muted small">Industry Focus</h6>
                        <p className="mb-0">
                        {founderData.curr_startup_industry}
                        {founderData.ai_in_curr_startup === 1 && (
                            <span className="badge bg-info ms-2">AI</span>
                        )}
                        </p>
                    </div>
                    )}
                    
                    {/* Experience */}
                    <div className="mb-3">
                        <h6 className="text-uppercase text-muted small">Experience</h6>
                        <p className="mb-0">
                            {founderData.was_prev_founder === 1 && (
                            <span className="d-block">Previous Founder</span>
                            )}

                            {founderData.was_in_accelerator === 1 && hasValue(founderData.accelerators_worked_in) && (
                            <p className="mb-0">
                                Accelerator:{" "}
                                {Array.isArray(founderData.accelerators_worked_in)
                                ? founderData.accelerators_worked_in.join(', ')
                                : JSON.parse(founderData.accelerators_worked_in).join(', ')
                                }
                                <span className="badge bg-info ms-2">Accelerator</span>
                            </p>
                            )}

                            {founderData.was_in_scaleup === 1 && hasValue(founderData.scaleups_worked_in) && (
                            <p className="mb-0">
                                Scaleup:{" "}
                                {Array.isArray(founderData.scaleups_worked_in)
                                ? founderData.scaleups_worked_in.join(', ')
                                : JSON.parse(founderData.scaleups_worked_in).join(', ')
                                }
                                <span className="badge bg-success ms-2">Scaleup</span>
                            </p> 
                            )}

                            {founderData.was_in_bigtech === 1 && hasValue(founderData.bigtechs_worked_in) && (
                            <p className="mb-0">
                                {" "}
                                {Array.isArray(founderData.bigtechs_worked_in)
                                    ? founderData.bigtechs_worked_in.join(', ')
                                    : JSON.parse(founderData.bigtechs_worked_in).join(', ')
                                } 
                                <span className="badge bg-primary ms-2">Big Tech</span>
                            </p>
                            )}
                        </p>
                    </div>
                    
                    {/* Tags */}
                    {hasValue(founderData.tags) && (
                    <div className="mb-4">
                        <h6 className="text-uppercase text-muted small">Tags</h6>
                        <div>
                        {Array.isArray(founderData.tags) ? (
                            founderData.tags.map((tag, index) => (
                            <span key={index} className="badge bg-secondary me-1 mb-1">{tag}</span>
                            ))
                        ) : (
                            <span className="badge bg-secondary me-1 mb-1">{founderData.tags}</span>
                        )}
                        </div>
                    </div>
                    )}
                    
                    {/* Contact Links */}
                    <div className="d-grid gap-2">
                    {hasValue(founderData.linkedin_url) && (
                        <a 
                        href={founderData.linkedin_url} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        className="btn btn-outline-primary"
                        >
                        <i className="bi bi-linkedin"></i> View LinkedIn Profile
                        </a>
                    )}
                    <a href="#" className="btn btn-outline-secondary">
                        <i className="bi bi-envelope"></i> Contact
                    </a>
                    </div>
                </div>
                </div>
                
                {/* Diversity Information Card */}
                <div className="card shadow-sm mb-4">
                <div className="card-header bg-light">
                    <h5 className="card-title mb-0">Diversity Information</h5>
                </div>
                <div className="card-body">
                    {hasValue(founderData.gender) && (
                    <div className="mb-3">
                        <h6 className="text-uppercase text-muted small">Gender</h6>
                        <p className="mb-0">{founderData.gender}</p>
                    </div>
                    )}
                    
                    {/* Migrant Status */}
                    {founderData.migrant === 1 && (
                    <div className="mb-3">
                        <h6 className="text-uppercase text-muted small">Migrant Status</h6>
                        <p className="mb-0">Migrant</p>
                    </div>
                    )}
                </div>
                </div>
            </div>
            
            <div className="col-md-8">
                {/* Professional Background Card */}
                <div className="card shadow-sm mb-4">
                <div className="card-header bg-light">
                    <h5 className="card-title mb-0">Professional Background</h5>
                </div>
                <div className="card-body">
                    {/* Founded Companies */}
                    {hasValue(founderData.all_founded_companies) && (
                    <div className="mb-4">
                        <h6 className="text-uppercase text-muted small">Founded Companies</h6>
                        <ul className="list-unstyled">
                        {(Array.isArray(founderData.all_founded_companies)
                            ? founderData.all_founded_companies
                            : JSON.parse(founderData.all_founded_companies)
                        ).map((company, index) => (
                            <li key={index} className="mb-2">
                            {typeof company === 'string' ? (
                                company
                            ) : (
                                <>
                                <strong>{company.name}</strong>
                                {company.year && <span className="text-muted ms-2">({company.year})</span>}
                                {company.exit && <span className="badge bg-success ms-2">{company.exit}</span>}
                                {company.status && <span className="badge bg-primary ms-2">{company.status}</span>}
                                </>
                            )}
                            </li>
                        ))}
                        </ul>
                    </div>
                    )}
                    
                    {/* Previous Companies */}
                    {(founderData.was_in_accelerator === 1 || 
                    founderData.was_in_scaleup === 1 || 
                    founderData.was_in_bigtech === 1) && (
                    <div className="mb-4">
                        <h6 className="text-uppercase text-muted small">Previous Companies</h6>

                        {founderData.was_in_accelerator === 1 && hasValue(founderData.accelerators_worked_in) && (
                        <p>
                            <strong>
                            {Array.isArray(founderData.accelerators_worked_in)
                                ? founderData.accelerators_worked_in.join(', ')
                                : JSON.parse(founderData.accelerators_worked_in).join(', ')
                            }
                            </strong>{" "}
                            <span className="badge bg-info">Accelerator</span>
                        </p>
                        )}

                        {founderData.was_in_scaleup === 1 && hasValue(founderData.scaleups_worked_in) && (
                        <p>
                            <strong>
                            {Array.isArray(founderData.scaleups_worked_in)
                                ? founderData.scaleups_worked_in.join(', ')
                                : JSON.parse(founderData.scaleups_worked_in).join(', ')
                            }
                            </strong>{" "}
                            <span className="badge bg-success">Scaleup</span>
                        </p>
                        )}

                        {founderData.was_in_bigtech === 1 && hasValue(founderData.bigtechs_worked_in) && (
                        <p>
                            <strong>
                            {Array.isArray(founderData.bigtechs_worked_in)
                                ? founderData.bigtechs_worked_in.join(', ')
                                : JSON.parse(founderData.bigtechs_worked_in).join(', ')
                            }
                            </strong>{" "}
                            <span className="badge bg-primary">Big Tech</span>
                        </p>
                        )}
                    </div>
                    )}
                    
                    {/* Education */}
                    {hasValue(founderData.top_degree) && (
                    <div className="mb-4">
                        <h6 className="text-uppercase text-muted small">Education</h6>
                        <ul className="list-unstyled">
                        <li className="mb-2">
                            <strong>{founderData.top_degree}</strong>
                            {hasValue(founderData.top_degree_label) && (
                            <span className="badge bg-secondary ms-2">{founderData.top_degree_label}</span>
                            )}
                            {hasValue(founderData.top_degree_end_date) && (
                            <span className="d-block text-muted small">
                                Completed {formatDate(founderData.top_degree_end_date)}
                            </span>
                            )}
                        </li>
                        </ul>
                    </div>
                    )}
                </div>
                </div>
            </div>
            </div>
        </div>
    )
}