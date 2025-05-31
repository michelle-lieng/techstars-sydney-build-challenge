import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './input.css'

import App from './App'
import Home from './pages/Home'
import Search from './pages/Search'

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        errorElement: <div>Something went wrong</div>,
        children: [
            {
                index: true,
                element: <Home />
            }, {
                path: '/search',
                element: <Search />
            }
        ]
    }
])

ReactDOM.createRoot(document.getElementById('root')).render(
    <RouterProvider router={router} />
)