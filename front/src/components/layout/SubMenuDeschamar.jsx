import styles from "./Menu.module.css"
import axios from "axios"


function SubMenuDeschamar (props) {

    const deschamar = async (numeroCamara) => {
        const resposta = await axios.get(`http://127.0.0.1:5001/deschamar/${numeroCamara}`)
        window.location.reload()
    }

    return (
        <div className={`${styles.divMenu} cor-fundo2`}>
            {props.camaras.map((camara, indice) => (
                <a onClick={() => deschamar(camara["numero_camara"].toLowerCase())}>
                    <button>DESCHAMAR CAM {camara["numero_camara"]}</button>
                </a>
            ))}
        </div>
    
    )
}

export default SubMenuDeschamar