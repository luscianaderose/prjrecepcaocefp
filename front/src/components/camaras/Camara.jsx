import styles from "./Camara.module.css"
import chamarComSomPng from "../../assets/img/chamar-com-som.png"
import chamarSemSomPng from "../../assets/img/chamar-sem-som.png"

function Camara(props){
    return(
        <div className={`${styles.dvpCamaraIndividual} cor-fundo2`}>
            <p>
                <div className={styles.dvpBtNumGdeComBtChamNov}>
                    {/* <!-- {bt_camara_num_gde} --> */}
                    <a style={{textDecoration:"none"}} href={`/abrir_camara/${props.numero}`}></a>

                    <div className={`${styles.dvpCamaraNumeroGrande} cor-${props.atividade}`}>
                        {props.numero}
                    </div>

                    <div className={styles.dvpBtChamarNovamente}>
                        <a className={styles.linkIcone} href={`/chamar_novamente/${props.numero}`}>
                            <img alt="Som" src={chamarComSomPng} width="16" height="16"/>
                        </a>
                        <a className={styles.linkIcone} href={`/chamar_novamente_sem_som/${props.numero}`}>
                            <img alt="Sem som" src={chamarSemSomPng} width="16" height="16"/>
                        </a>
                    </div>
                </div>
            </p>

            {/* <!-- {camara.estado}<br> --> */}
            <span className={styles.iconeFechada}></span> FECHADA<br></br>
            <p className="txt-destaque">CÂMARA VAZIA</p>
            <p className="atendimentos txt-pequeno b">ATENDIMENTOS</p>
            <a className={`${styles.linkBolinhas} a`} href={`/bolinhas?modo=subtracao&numero_camara=${props.numero}`}>
                <b>-</b>
            </a>
            {/* <!-- {camara.bolinhas()} --> */}
            {String.fromCharCode(9898)}
            {String.fromCharCode(9898)}
            {String.fromCharCode(9898)}
            {String.fromCharCode(9898)}
            {String.fromCharCode(9898)}
            <a className={`${styles.linkBolinhas} a`} href={`/bolinhas?modo=adicao&numero_camara=${props.numero}`}>
                <b>+</b>
            </a>
            {/* <!-- {bt_camara} --> */}
            <p>
                <button type="button">
                    <a className={`${styles.btCamara} a`} href={`/abrir_camara/${props.numero}`}>ABRIR CÂMARA</a>
                </button>
            </p>
        </div>
    )
}

export default Camara