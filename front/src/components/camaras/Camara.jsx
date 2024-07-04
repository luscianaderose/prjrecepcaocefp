import styles from "./Camara.module.css"
import chamarComSomPng from "../../assets/img/chamar-com-som.png"
import chamarSemSomPng from "../../assets/img/chamar-sem-som.png"
import CamaraBotao from "./CamaraBotao"
import CamaraIcone from "./CamaraIcone"
import CamaraBolinhas from "./CamaraBolinhas"

function Camara(props){
    // console.log(props.numero, props.atividade)
    // console.log("pessoa em atendimento:", props.pessoaEmAtendimento, props.fila)
    // if (props.pessoaEmAtendimento !== null){
    //     console.log(props.pessoaEmAtendimento["nome"], props.pessoaEmAtendimento["dupla"])
    // }
    const classeCamara = {
        "fechada":"camara-fechada",
        "atendendo":"camara-chamando",
        "último":"camara-avisar",
        "foi avisado":"camara-avisado"
    }

    return(
        <div className={`${styles.dvpCamaraIndividual} cor-fundo2 ${classeCamara[props.estado.toLowerCase()]}`}>
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
            {/* <span className={styles.iconeFechada}></span> FECHADA<br></br> */}
            {props && <CamaraIcone estado={props.estado}/>}
            <p className="txt-destaque">{props.pessoaEmAtendimento ? `${props.numeroAtendimentos}. ${props.pessoaEmAtendimento["nome"]}` : "CÂMARA VAZIA"}</p>
            <p className="atendimentos txt-pequeno b">ATENDIMENTOS</p>
            <CamaraBolinhas 
                numero={props.numero}
                capacidade={props.capacidade}
                numeroAtendimentos={props.numeroAtendimentos}
            />
            {/* <!-- {bt_camara} --> */}
            <p>
                <CamaraBotao numero={props.numero} estado={props.estado}/>
            </p>
        </div>
    )
}

export default Camara