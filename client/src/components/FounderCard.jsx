import React from 'react';

export default function FounderCard({ founder }) {
  return (
    <div className="col-md-6 mb-4">
      <div className="card h-100 founder-card">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-start">
            <h5 className="card-title founder-name mb-0">{founder.name}</h5>
            <span className="badge bg-success founder-completeness">
              {founder.profile_completeness}%
            </span>
          </div>
          <p className="text-muted mb-2">
            <i className="bi bi-geo-alt"></i> {founder.city}
          </p>
          <p className="founder-role mb-2">{founder.role}</p>
          <p className="founder-startup small mb-2">{founder.startup}</p>
          <div className="founder-tags mb-3">
            {founder.tags && founder.tags.map((tag, index) => (
              <span key={index} className="badge bg-secondary me-1">{tag}</span>
            ))}
          </div>
          <div className="diversity-badges mb-3">
            {founder.diversity && founder.diversity.map((badge, index) => (
              <span key={index} className="badge bg-info me-1">{badge}</span>
            ))}
          </div>
          <a href={`/profile/${founder.id}`} className="btn btn-sm btn-outline-primary me-2">
            View Profile
          </a>
          <a href={founder.linkedin_url} className="btn btn-sm btn-outline-secondary" target="_blank" rel="noopener noreferrer">
            <i className="bi bi-linkedin"></i> LinkedIn
          </a>
        </div>
      </div>
    </div>
  );
}