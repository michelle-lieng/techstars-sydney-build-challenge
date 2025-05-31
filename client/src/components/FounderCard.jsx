export default function FounderCard() {
    return (
        <template id="founder-card-template">
            <div class="col-md-6 mb-4">
                <div class="card h-100 founder-card">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <h5 class="card-title founder-name mb-0"></h5>
                            <span class="badge bg-success founder-completeness"></span>
                        </div>
                        <p class="text-muted mb-2">
                            <i class="bi bi-geo-alt"></i> <span class="founder-city"></span>
                        </p>
                        <p class="founder-role mb-2"></p>
                        <p class="founder-startup small mb-2"></p>
                        <div class="founder-tags mb-3"></div>
                        <div class="diversity-badges mb-3"></div>
                        <a href="#" class="btn btn-sm btn-outline-primary view-profile">View Profile</a>
                        <a href="#" class="btn btn-sm btn-outline-secondary linkedin-profile" target="_blank">
                            <i class="bi bi-linkedin"></i> LinkedIn
                        </a>
                    </div>
                </div>
            </div>
        </template>        
    )
}