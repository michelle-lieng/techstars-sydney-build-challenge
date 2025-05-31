import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './input.css'
import App from './App'

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        errorElement: <div>Something went wrong</div>,
        children: [
            {
                index: true,
                element: <div>Home Page</div>
            }
        ]
    }
])

ReactDOM.createRoot(document.getElementById('root')).render(
    <RouterProvider router={router} />
)