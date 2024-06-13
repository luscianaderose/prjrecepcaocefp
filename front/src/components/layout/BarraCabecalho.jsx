import cefpPng from "../../assets/img/cefp.png"
import styles from "./BarraCabecalho.module.css"

function BarraCabecalho(){
    return(
        <div className={styles.divCabecalho}>
            <div className={styles.dcLogo}>
                <img alt="CONGREGAÇÃO ESPÍRITA FRANCISCO DE PAULA" src={cefpPng} height="50"/>
            </div>
            <div className={`${styles.dcTit} txt-tit1`}>RECEPÇÃO DAS CÂMARAS</div>
            <div className={styles.dcData}>
                <p className="txt-normal">QUINTA 06 JUNHO 18:33</p>
            </div>
        </div>
    )
}

export default BarraCabecalho