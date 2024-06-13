import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Recepcao from './pages/Recepcao'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Tv from './pages/Tv'

function App() {
    return (
    <>
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<Recepcao/>}/>
                <Route exact path="/tv" element={<Tv/>}/>
            </Routes>
        </BrowserRouter>
    </>
)
}

export default App
