import axios from "axios"
import { useState, useEffect } from "react"
import styles from "./Tvs.module.css"
import Tv from "./Tv"


function Tvs () {
    const [camaras, setCamaras] = useState()
    const [filaVidencia, setFilaVidencia] = useState()
    const [filaPrece, setFilaPrece] = useState()

    useEffect(() => {
        const buscarDados = async () => {
            const respostaCamara = await axios.get("http://127.0.0.1:5001/camaras")
            setCamaras(respostaCamara.data)
            const respostaFilaVidencia = await axios.get("http://127.0.0.1:5001/fila_videncia")
            setFilaVidencia(respostaFilaVidencia.data)
            const respostaFilaPrece = await axios.get("http://127.0.0.1:5001/fila_prece")
            setFilaPrece(respostaFilaPrece.data)
        }
        buscarDados()
    }, [])


    return (
        <div className={styles.tvVidenciaPrece}>
            <div className={`${styles.tvVidencia} cor-videncia`}>
                {/* TV VIDENCIA */}
                {/* <Tv numero="2" atividade="videncia"/>
                <Tv numero="4" atividade="videncia"/> */}
                {camaras && Object.values(camaras).map((camara, indice) => (
                    
                    // console.log("camara nome fila, numero camara, nome display, estado", camara["nome_fila"], camara["numero_camara"], camara["fila"]["nome_display"], camara["estado"])

                    camara["nome_fila"] === "videncia" && 
                    <Tv 
                        numero={camara["numero_camara"]} 
                        atividade={camara["fila"]["nome_display"]} 
                        estado={camara["estado"]}
                        pessoaAtendida={camara["pessoa_em_atendimento"]}
                        fila={filaVidencia}
                    />
                ))}
            </div>
            <div className={`${styles.tvPrece} cor-prece`}>
                {/* TV PRECE */}
                {camaras && Object.values(camaras).map((camara, indice) => (
                    camara["nome_fila"] === "prece" && 
                    <Tv 
                        numero={camara["numero_camara"]} 
                        atividade={camara["fila"]["nome_display"]} 
                        estado={camara["estado"]}
                        pessoaAtendida={camara["pessoa_em_atendimento"]}
                        fila={filaPrece}
                    />
                ))}
            </div>

        </div>
    )
}

export default Tvs