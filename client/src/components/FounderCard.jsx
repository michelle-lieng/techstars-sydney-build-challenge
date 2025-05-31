export default function FounderCard() {
    return (
        <template id="founder-card-template">
            <div className="col-md-6 mb-4">
                <div className="card h-100 founder-card">
                    <div className="card-body">
                        <div className="d-flex justify-content-between align-items-start">
                            <h5 className="card-title founder-name mb-0"></h5>
                            <span className="badge bg-success founder-completeness"></span>
                        </div>
                        <p className="text-muted mb-2">
                            <i className="bi bi-geo-alt"></i> <span className="founder-city"></span>
                        </p>
                        <p className="founder-role mb-2"></p>
                        <p className="founder-startup small mb-2"></p>
                        <div className="founder-tags mb-3"></div>
                        <div className="diversity-badges mb-3"></div>
                        <a href="#" className="btn btn-sm btn-outline-primary view-profile">View Profile</a>
                        <a href="#" className="btn btn-sm btn-outline-secondary linkedin-profile" target="_blank">
                            <i className="bi bi-linkedin"></i> LinkedIn
                        </a>
                    </div>
                </div>
            </div>
        </template>        
    )
}