import axios from "axios"
import styles from "./Menu.module.css"


function SubMenuDiminuir (props) {

    const diminuir = async (numeroCamara) => {
        const resposta = await axios.get(`http://127.0.0.1:5001/diminuir_capacidade/${numeroCamara}`)
        window.location.reload()
    }

    return (
        <div className={`${styles.divMenu} cor-fundo2`}>
            {props.camaras.map((camara, indice) => (
                <a onClick={() => diminuir(camara["numero_camara"].toUpperCase())}>
                    <button>DIMINUIR CAM {camara["numero_camara"]}</button>
                </a>
            ))}
        </div>
    
    )
}

export default SubMenuDiminuir