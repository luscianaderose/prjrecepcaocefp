import styles from "./Menu.module.css"
import SubMenuDeschamar from "./SubMenuDeschamar"
import axios from "axios"
import { useState, useEffect } from "react"
import SubMenuAumentar from "./SubMenuAumentar"
import SubMenuDiminuir from "./SubMenuDiminuir"
import SubMenuGeral from "./SubMenuGeral"


function Menu(){

    const [camaras, setCamaras] = useState()

    useEffect(
        () => {
            const buscarCamaras = async () => {
                try {
                    const resposta = await axios.get("http://127.0.0.1:5001/camaras")
                    const dados = await resposta.data
                    setCamaras(dados)
                    console.log(dados)
                } catch(error){
                    console.error("erro", error)
                }
            }
            buscarCamaras()
        }
        ,[]
    )

    return(
        <div className={`${styles.divMenuTodo} cor-fundo2`}>
            {/* <!-- tit_menu --> */}
            <p className="txt-tit2">MENU</p>

            <SubMenuGeral/>
            {camaras && <SubMenuDeschamar camaras={camaras}/>}
            {camaras && <SubMenuAumentar camaras={camaras}/>}
            {camaras && <SubMenuDiminuir camaras={camaras}/>}
        </div>

    )
}

export default Menu