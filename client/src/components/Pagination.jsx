export default function Pagination({ currentPage, totalPages, setCurrentPage }) {
    return (
        <nav>
            <ul className="pagination">
                <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                    <button
                        className="page-link"
                        onClick={() => setCurrentPage(currentPage - 1)}
                        disabled={currentPage === 1}
                    >
                        Previous
                    </button>
                </li>

                {[...Array(totalPages)].map((_, index) => (
                    <li key={index} className={`page-item ${currentPage === index + 1 ? 'active' : ''}`}>
                        <button
                            className="page-link"
                            onClick={() => setCurrentPage(index + 1)}
                        >
                            {index + 1}
                        </button>
                    </li>
                ))}

                <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                    <button
                        className="page-link"
                        onClick={() => setCurrentPage(currentPage + 1)}
                        disabled={currentPage === totalPages}
                    >
                        Next
                    </button>
                </li>
            </ul>
        </nav>
    )
}