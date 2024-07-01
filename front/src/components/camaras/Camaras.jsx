import styles from "./Camaras.module.css"
import Camara from "./Camara"
import Fila from "../filas/Fila"
import axios from "axios"
import { useState, useEffect } from "react"

function Camaras(){
    const [camaras, setCamaras] = useState()
    const [filaVidencia, setFilaVidencia] = useState()
    const [filaPrece, setFilaPrece] = useState()

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

            const buscarFilas = async () => {
                try {
                    const respostaFilaVidencia = await axios.get("http://127.0.0.1:5001/fila_videncia")
                    const respostaFilaPrece = await axios.get("http://127.0.0.1:5001/fila_prece")
                    setFilaVidencia(respostaFilaVidencia.data)
                    setFilaPrece(respostaFilaPrece.data)
                    console.log("respostaFilaVidencia", respostaFilaVidencia.data)
                    console.log("respostaFilapRrece", respostaFilaPrece.data)
                } catch(error){
                    console.error("erro", error)
                }
            }
            buscarFilas()
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
                                pessoaEmAtendimento={camara["pessoa_em_atendimento"]}
                            />
                        )
                    ))}
                </div>
                {filaVidencia && <Fila atividade="videncia" fila={filaVidencia}/>}
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
                                pessoaEmAtendimento={camara["pessoa_em_atendimento"]}
                            />
                        )
                    ))}
                </div>
                {filaPrece && <Fila atividade="prece" fila={filaPrece}/>}
            </div>
        </div>
    )
}

export default Camaras