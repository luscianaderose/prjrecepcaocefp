import styles from "./Camaras.module.css"
import Camara from "./Camara"
import Fila from "../filas/Fila"

function Camaras(){
    return(
        <div className={styles.divVidenciaPrece}>
            <div className={styles.divVidencia}>
                <div className={`${styles.dvpTit} txt-tit2 cor-videncia`}>CÂMARAS VIDÊNCIA</div>
                <div className={`${styles.dvpCamaraTotal} cor-videncia`}>
                    <Camara atividade="videncia" numero="2"/>
                    <Camara atividade="videncia" numero="4"/>
                </div>
                <Fila atividade="videncia"/>
            </div>
            <div className={styles.divEspaco}> </div>
            <div className={styles.divPrece}>
                <div className={`${styles.dvpTit} txt-tit2 cor-prece`}>CÂMARAS PRECE</div>
                <div className={`${styles.dvpCamaraTotal} cor-prece`}>
                    <Camara atividade="prece" numero="3"/>
                    <Camara atividade="prece" numero="3A"/>
                </div>
                <Fila atividade="prece"/>
            </div>
        </div>
    )
}

export default Camaras