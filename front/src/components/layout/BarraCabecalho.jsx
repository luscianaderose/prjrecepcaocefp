import cefpPng from "../../assets/img/cefp.png"
import styles from "./BarraCabecalho.module.css"
import { useState, useEffect } from "react"
import axios from "axios"


function BarraCabecalho(){
    const [dataEHora, setDataEHora] = useState()
    useEffect(
        () => {
            const buscarDataEHora = async () => {
                const response = await axios.get("http://127.0.0.1:5001/calendario")
                const data = await response.data
                setDataEHora(data["data_e_hora"])
                console.log(data["data_e_hora"])
            }
            buscarDataEHora()
        }, []
    )


    return(
        <div className={styles.divCabecalho}>
            <div className={styles.dcLogo}>
                <img alt="CONGREGAÇÃO ESPÍRITA FRANCISCO DE PAULA" src={cefpPng} height="50"/>
            </div>
            <div className={`${styles.dcTit} txt-tit1`}>RECEPÇÃO DAS CÂMARAS</div>
            <div className={styles.dcData}>
                <p className="txt-normal">{dataEHora ? dataEHora : "Carregando..."}</p>
            </div>
        </div>
    )
}

export default BarraCabecalho