export default function Home() {
    return (
        <main>
            <div class="container mt-5">
                <div class="row">
                    <div class="col-md-6">
                        <h1 class="display-4">Discover Australia's Hidden Founders</h1>
                        <p class="lead">Find and connect with high-potential current and future founders across Australia.</p>
                        <p class="mb-4">Our searchable database helps you discover diverse talent that's building the next wave of innovation - from scale-up veterans to PhD researchers with IP ready to spin out.</p>
                        <div class="d-grid gap-2 d-md-flex">
                            <a href="/search" class="btn btn-primary btn-lg px-4 me-md-2">Start Searching</a>
                            <a href="/stats" class="btn btn-outline-primary btn-lg px-4">View Statistics</a>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card shadow-lg">
                            <div class="card-body p-4">
                                <h2 class="card-title mb-4">Quick Search</h2>
                                <form id="quick-search-form">
                                    <div class="mb-3">
                                        <label for="name" class="form-label">Name or Keyword</label>
                                        <input type="text" class="form-control" id="name" placeholder="Enter name or keyword"/>
                                    </div>
                                    <div class="mb-3">
                                        <label for="city" class="form-label">City</label>
                                        <select class="form-select" id="city">
                                            <option value="">All Cities</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="tag" class="form-label">Founder Type</label>
                                        <select class="form-select" id="tag">
                                            <option value="">All Types</option>
                                        </select>
                                    </div>
                                    <div class="d-grid">
                                        <button type="submit" class="btn btn-primary">Search</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row mt-5">
                    <div class="col-12">
                        <h2 class="text-center mb-4">Why Hidden Founders?</h2>
                    </div>
                    <div class="col-md-4">
                        <div class="card h-100 border-0 shadow-sm">
                            <div class="card-body text-center p-4">
                                <div class="feature-icon bg-primary bg-gradient text-white rounded-circle mb-3">
                                    <i class="bi bi-search"></i>
                                </div>
                                <h3>Discover Talent</h3>
                                <p>Find high-potential founders before they're headlines. Our database surfaces talent that's not yet visible in traditional networks.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card h-100 border-0 shadow-sm">
                            <div class="card-body text-center p-4">
                                <div class="feature-icon bg-primary bg-gradient text-white rounded-circle mb-3">
                                    <i class="bi bi-bar-chart"></i>
                                </div>
                                <h3>Diversity Insights</h3>
                                <p>Access detailed diversity metrics including gender, ethnicity, and migrant status to build more inclusive founder communities.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card h-100 border-0 shadow-sm">
                            <div class="card-body text-center p-4">
                                <div class="feature-icon bg-primary bg-gradient text-white rounded-circle mb-3">
                                    <i class="bi bi-filter"></i>
                                </div>
                                <h3>Advanced Filtering</h3>
                                <p>Filter by expertise, background, location, and more to find exactly the founder profiles you're looking for.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row mt-5">
                    <div class="col-12">
                        <h2 class="text-center mb-4">Featured Founder Categories</h2>
                    </div>
                    <div class="col-md-3">
                        <div class="card category-card mb-4">
                            <div class="card-body">
                                <h3 class="h5">Scale-up Alumni</h3>
                                <p class="small">Experienced professionals from Australia's fastest-growing companies</p>
                                <a href="/search?tags=scale-up+alum" class="stretched-link"></a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card category-card mb-4">
                            <div class="card-body">
                                <h3 class="h5">PhD Researchers</h3>
                                <p class="small">Academic innovators with IP ready for commercialization</p>
                                <a href="/search?tags=PhD+researcher" class="stretched-link"></a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card category-card mb-4">
                            <div class="card-body">
                                <h3 class="h5">Side Project Builders</h3>
                                <p class="small">Creators developing innovative products while employed</p>
                                <a href="/search?tags=side+project+builder" class="stretched-link"></a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card category-card mb-4">
                            <div class="card-body">
                                <h3 class="h5">Migrant Founders</h3>
                                <p class="small">International entrepreneurs building in Australia</p>
                                <a href="/search?tags=migrant+founder" class="stretched-link"></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>         
        </main>
    )
}