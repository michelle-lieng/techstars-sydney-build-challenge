export default function Search() {
    return (
        <main>
            <div class="container mt-4">
                <div class="row">
                    <div class="col-12">
                        <h1>Search Hidden Founders</h1>
                        <p class="lead">Find high-potential founders across Australia using advanced filters.</p>
                    </div>
                </div>

                <div class="row mt-3">
                    <div class="col-md-3">
                        <div class="card shadow-sm mb-4">
                            <div class="card-header bg-light">
                                <h5 class="card-title mb-0">Filters</h5>
                            </div>
                            <div class="card-body">
                                <form id="search-form">
                                    <div class="mb-3">
                                        <label for="search-name" class="form-label">Name</label>
                                        <input type="text" class="form-control" id="search-name" placeholder="Enter name"/>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="search-city" class="form-label">City</label>
                                        <select class="form-select" id="search-city">
                                        </select>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="search-startup" class="form-label">Startup Name</label>
                                        <input type="text" class="form-control" id="search-startup" placeholder="Enter startup name"/>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="form-label">Founder Type</label>
                                        <div class="tags-container" id="tags-container">
                                            {/* {% for tag in tags %}
                                            <div class="form-check">
                                                <input class="form-check-input tag-checkbox" type="checkbox" value="{{ tag.name }}" id="tag-{{ tag.id }}">
                                                <label class="form-check-label" for="tag-{{ tag.id }}">
                                                    {{ tag.name }}
                                                </label>
                                            </div>
                                            {% endfor %} */}
                                        </div>
                                    </div>
                                    
                                    <hr/>
                                    
                                    <h6 class="mb-3">Diversity Filters</h6>
                                    
                                    <div class="mb-3">
                                        <label for="search-gender" class="form-label">Gender</label>
                                        <select class="form-select" id="search-gender">
                                            <option value="">All Genders</option>
                                            <option value="Female">Female</option>
                                            <option value="Male">Male</option>
                                            <option value="Non-binary">Non-binary</option>
                                        </select>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="search-ethnicity" class="form-label">Ethnicity</label>
                                        <select class="form-select" id="search-ethnicity">
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
                                    
                                    <div class="mb-3">
                                        <label for="search-migrant" class="form-label">Migrant Status</label>
                                        <select class="form-select" id="search-migrant">
                                            <option value="">All</option>
                                            <option value="true">Migrant Founders</option>
                                            <option value="false">Non-Migrant Founders</option>
                                        </select>
                                    </div>
                                    
                                    <div class="d-grid">
                                        <button type="submit" class="btn btn-primary">Apply Filters</button>
                                        <button type="button" class="btn btn-outline-secondary mt-2" id="reset-filters">Reset Filters</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-9">
                        <div class="card shadow-sm mb-4">
                            <div class="card-header bg-light d-flex justify-content-between align-items-center">
                                <h5 class="card-title mb-0">Results <span id="result-count" class="badge bg-primary ms-2">0</span></h5>
                                <div class="d-flex align-items-center">
                                    <label for="sort-by" class="form-label me-2 mb-0">Sort by:</label>
                                    <select class="form-select form-select-sm" id="sort-by" style="width: auto;">
                                        <option value="profile_completeness">Completeness</option>
                                        <option value="name">Name</option>
                                        <option value="city">City</option>
                                    </select>
                                </div>
                            </div>
                            <div class="card-body">
                                <div id="search-results" class="row">
                                    <div class="col-12 text-center py-5">
                                        <div class="spinner-border text-primary" role="status">
                                            <span class="visually-hidden">Loading...</span>
                                        </div>
                                        <p class="mt-3">Loading founders...</p>
                                    </div>
                                </div>
                                
                                <div id="pagination" class="d-flex justify-content-center mt-4">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>            
        </main>
    )
}