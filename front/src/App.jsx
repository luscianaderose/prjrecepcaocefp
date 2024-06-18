import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Recepcao from './pages/Recepcao'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Tv from './pages/Tv'

function App() {
    // jeito errado
    var numero = 0 

    const somarUm = () => {
        numero = numero + 1
        console.log("numero:", numero)
    }

    // jeito certo
    const [numero2, setNumero2] = useState(0)

    const somarUmCerto = () => {
        setNumero2(numero2 + 1)
        console.log("numero:", numero2)
    }

    // use Effect 
    useEffect(  
        //função anônima
        () => (console.log("oi")), [numero2]
    )

    return (
    <>
        {/* <p>{numero2}</p>
        <button onClick={() => somarUmCerto()}>click</button> */}
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
