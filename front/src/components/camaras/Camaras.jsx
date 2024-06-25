import styles from "./Camaras.module.css"
import Camara from "./Camara"
import Fila from "../filas/Fila"
import axios from "axios"
import { useState, useEffect } from "react"

function Camaras(){
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
        <div className={styles.divVidenciaPrece}>
            <div className={styles.divVidencia}>
                <div className={`${styles.dvpTit} txt-tit2 cor-videncia`}>CÂMARAS VIDÊNCIA</div>
                <div className={`${styles.dvpCamaraTotal} cor-videncia`}>
                    {camaras && camaras.map((camara, indice) => (
                        camara["nome_fila"] === "videncia" && (
                            <Camara 
                                atividade={camara["nome_fila"]} 
                                numero={camara["numero_camara"]} 
                                estado={camara["estado"]}
                                capacidade={camara["capacidade_maxima"]}
                                numeroAtendimentos={camara["numero_de_atendimentos"]}
                            />
                        )
                    ))}
                </div>
                <Fila atividade="videncia"/>
            </div>
            <div className={styles.divEspaco}> </div>
            <div className={styles.divPrece}>
                <div className={`${styles.dvpTit} txt-tit2 cor-prece`}>CÂMARAS PRECE</div>
                <div className={`${styles.dvpCamaraTotal} cor-prece`}>
                    {camaras && camaras.map((camara, indice) => (
                        camara["nome_fila"] === "prece" && (
                            <Camara 
                                atividade={camara["nome_fila"]} 
                                numero={camara["numero_camara"]} 
                                estado={camara["estado"]}
                                capacidade={camara["capacidade_maxima"]}
                                numeroAtendimentos={camara["numero_de_atendimentos"]}
                            />
                        )
                    ))}
                </div>
                <Fila atividade="prece"/>
            </div>
        </div>
    )
}

export default Camaras