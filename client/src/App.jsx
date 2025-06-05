import { Outlet } from 'react-router-dom'
import {
    ApolloClient,
    InMemoryCache,
    ApolloProvider,
    createHttpLink,
} from '@apollo/client'

import Header from "./components/Header"
import Footer from "./components/Footer"

const httpLink = createHttpLink({
    uri: '/graphql',
})

const client = new ApolloClient({
    link: httpLink,
    cache: new InMemoryCache(),
})

function App() {
    return  (
        <ApolloProvider client={client}>
            <Header />
            <Outlet />
            <Footer />
        </ApolloProvider>
    )
}

export default App;