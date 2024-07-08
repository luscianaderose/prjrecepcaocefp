import axios from "axios"
import styles from "./Menu.module.css"


function SubMenuDeschamar (props) {

    const deschamar = async (numeroCamara, estadoCamara, numeroAtendendo) => {
        if (estadoCamara === "FECHADA"){
            alert("Não é possível deschamar porque a câmara está fechada! Seu bobo!")
        }else if(numeroAtendendo === null){
            alert("Não é possível deschamar porque não há ninguém para deschamar!")
        }else{
            const resposta = await axios.get(`http://127.0.0.1:5001/deschamar/${numeroCamara}`)
            window.location.reload()
        }
    }

    return (
        <div className={`${styles.divMenu} cor-fundo2`}>
            {props.camaras.map((camara, indice) => (
                <a onClick={() => deschamar(camara["numero_camara"].toUpperCase(), camara["estado"].toUpperCase(), camara["pessoa_em_atendimento"])}>
                    <button>DESCHAMAR CAM {camara["numero_camara"]}</button>
                </a>
            ))}
        </div>
    
    )
}

export default SubMenuDeschamar