import styles from "./Camara.module.css"
import chamarComSomPng from "../../assets/img/chamar-com-som.png"
import chamarSemSomPng from "../../assets/img/chamar-sem-som.png"
import CamaraBotao from "./CamaraBotao"
import CamaraIcone from "./CamaraIcone"
import CamaraBolinhas from "./CamaraBolinhas"
import audioCamara2Wav from "../../assets/audio/camara2.wav"
import audioCamara3Wav from "../../assets/audio/camara3.wav"
import audioCamara3AWav from "../../assets/audio/camara3A.wav"
import audioCamara4Wav from "../../assets/audio/camara4.wav"

const audiosCamara = {
    "2":audioCamara2Wav,
    "4":audioCamara4Wav,
    "3":audioCamara3Wav,
    "3A":audioCamara3AWav
}

function Camara(props){
    // console.log(props.numeroCamara, props.atividade)
    // console.log("pessoa em atendimento:", props.pessoaEmAtendimento, props.fila)
    // if (props.pessoaEmAtendimento !== null){
    //     console.log(props.pessoaEmAtendimento["nome"], props.pessoaEmAtendimento["dupla"])
    // }

    // console.log("propriedades:", props.pessoaEmAtendimento)

    var nomeDupla = ""
    var numeroAtendidoNaFila = ""
    if (typeof props.fila === "object" && "fila" in props.fila && props.pessoaEmAtendimento !== null){
        numeroAtendidoNaFila = Object.keys(props.fila["fila"]).indexOf(props.pessoaEmAtendimento["numero"].toString()) + 1
        // console.log("numero atendido na fila:", props.pessoaEmAtendimento["numero"])
        // console.log("número do atendido oficial:", Object.keys(props.fila["fila"]).indexOf(props.pessoaEmAtendimento["numero"].toString()) + 1)
        // console.log("lista do numero das pessoas:", Object.keys(props.fila["fila"]))
    }

    if (props.pessoaEmAtendimento && props.pessoaEmAtendimento["dupla"] !== -1) {
        // console.log("pessoa em atendimento com dupla")
        if (typeof props.fila === "object" && "fila" in props.fila){
            const indice = props.pessoaEmAtendimento["dupla"]
            // console.log("indice:", indice)
            nomeDupla = props.fila["fila"][indice]["nome"]
            // console.log("nome dupla:", nomeDupla)
        }
    }

    const classeCamara = {
        "fechada":"camara-fechada",
        "atendendo":"camara-chamando",
        "último":"camara-avisar",
        "foi avisado":"camara-avisado"
    }

    const chamarNovamente = () => {
        const audio = new Audio(audiosCamara[props.numeroCamara])
        audio.play()
    }

    return(
        <div className={`${styles.dvpCamaraIndividual} cor-fundo2 ${classeCamara[props.estado.toLowerCase()]}`}>
            <p>
                <div className={styles.dvpBtNumGdeComBtChamNov}>
                    {/* <!-- {bt_camara_num_gde} --> */}
                    <a style={{textDecoration:"none"}} href={`/abrir_camara/${props.numeroCamara}`}></a>

                    <div className={`${styles.dvpCamaraNumeroGrande} cor-${props.atividade}`}>
                        {props.numeroCamara}
                    </div>

                    <div className={styles.dvpBtChamarNovamente}>
                        <a className={styles.linkIcone} onClick={() => chamarNovamente()}>
                            <img alt="Som" src={chamarComSomPng} width="16" height="16"/>
                        </a>
                        <a className={styles.linkIcone} href={`/chamar_novamente_sem_som/${props.numeroCamara}`}>
                            <img alt="Sem som" src={chamarSemSomPng} width="16" height="16"/>
                        </a>
                    </div>
                </div>
            </p>

            {/* <!-- {camara.estado}<br> --> */}
            {/* <span className={styles.iconeFechada}></span> FECHADA<br></br> */}
            {props && <CamaraIcone estado={props.estado}/>}
            <p className="txt-destaque">
                {props.pessoaEmAtendimento ? `${numeroAtendidoNaFila}. ${props.pessoaEmAtendimento["nome"]}` : "CÂMARA VAZIA"}
                {nomeDupla && ` & ${nomeDupla}`}
            </p>
            <p className="atendimentos txt-pequeno b">ATENDIMENTOS</p>
            <CamaraBolinhas 
                numero={props.numeroCamara}
                capacidade={props.capacidade}
                numeroAtendimentos={props.numeroAtendimentos}
            />
            {/* <!-- {bt_camara} --> */}
            <p>
                <CamaraBotao numero={props.numeroCamara} estado={props.estado}/>
            </p>
        </div>
    )
}

export default Camara