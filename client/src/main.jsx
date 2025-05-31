import ReactDom from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom/dist'
import './input.css'

import App from './App'

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        error: <Error />
    }
])

ReactDom.createRoot(document.getElementById('root')).render(
    <RouterProvider router={router} />
)