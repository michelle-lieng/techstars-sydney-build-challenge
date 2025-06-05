export default function MigrantDropdown() {
    return (
        <select className="form-select" id="search-migrant">
            <option value="">All</option>
            <option value="true">Migrant Founders</option>
            <option value="false">Non-Migrant Founders</option>
        </select>
    )
}