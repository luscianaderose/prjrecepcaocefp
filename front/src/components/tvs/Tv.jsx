import styles from "./Tv.module.css"
import CamaraBola from "../camaras/CamaraBola"


function Tv (props) {
    var nomeDupla = ""
    var nomeAtendido = ""
    var numeroAtendido = ""
    var filasNomesPessoas = []

    if (props.pessoaAtendida !== null){
        nomeAtendido = props.pessoaAtendida["nome"]
        if (props.pessoaAtendida["dupla"] !== -1 && props.fila !== undefined){
            const numeroDupla = props.pessoaAtendida["dupla"]
            nomeDupla = props.fila["fila"][numeroDupla]["nome"]
        }
    }

    if (props.fila !== undefined && nomeAtendido !== ""){
        Object.values(props.fila["fila"]).map((pessoa, indice) => (
            filasNomesPessoas.push(pessoa["nome"])
        ))
        numeroAtendido = filasNomesPessoas.indexOf(nomeAtendido)
    }

    const classeDaCamara = {
        "fechada":"camara-fechada",
        "atendendo":"camara-chamando",
        "último":"camara-avisar",
        "foi avisado":"camara-avisando"
    }

    return (
        <div className={`${styles.tvCamara} cor-fundo2 ${classeDaCamara[props.estado.toLowerCase()]}`}>
            <CamaraBola 
                className={`cor-${props.atividade} ${styles.camaraBolaTv}`}
                numeroCamara={props.numero}
            />
            <div className={styles.tvCamaraConteudo}>
                <div className={styles.tvCamaraFonteNumCamara}>
                    <div className={`txt-tv1 ${styles.bolaEAtividade}`}>
                        {props.label.toUpperCase()}
                    </div>
                </div>
                <p className="txt-tv2">{props.estado.toUpperCase()}</p>
                <p className="txt-tv2">
                    {nomeAtendido !== "" && `${numeroAtendido + 1}. ${nomeAtendido}`}
                    {nomeDupla !== "" && ` & ${nomeDupla}`}
                    {numeroAtendido === "" && "CÂMARA VAZIA"}
                </p>
            </div>
        </div>
    )
}

export default Tv