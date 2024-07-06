import styles from "./Tv.module.css"


function Tv (props) {
    var nomeDupla = ""
    var nomeAtendido = ""
    var numeroAtendido = ""
    var filasNomesPessoas = []

    if (props.pessoaAtendida !== null){
        nomeAtendido = props.pessoaAtendida["nome"]
        if (props.pessoaAtendida["dupla"] !== -1 && props.fila !== undefined){
            // console.log("dupla", props.pessoaAtendida["dupla"])
            const numeroDupla = props.pessoaAtendida["dupla"]
            nomeDupla = props.fila["fila"][numeroDupla]["nome"]
            // console.log("nome dupla:", nomeDupla)
        }
    }

    if (props.fila !== undefined && nomeAtendido !== ""){
        Object.values(props.fila["fila"]).map((pessoa, indice) => (
            filasNomesPessoas.push(pessoa["nome"])
        ))
        numeroAtendido = filasNomesPessoas.indexOf(nomeAtendido)
        // filasNomesPessoas = Object.values(props.fila["fila"]).map((pessoa, item) => [pessoa["nome"]])
    }
    // console.log("filas nomes pessoas:", filasNomesPessoas)
    // console.log("numero atendido:", numeroAtendido, nomeAtendido, props.numero)
    // console.log("pessoaAtendida:", props.pessoaAtendida)

    const classeDaCamara = {
        "fechada":"camara-fechada",
        "atendendo":"camara-chamando",
        "último":"camara-avisar",
        "foi avisado":"camara-avisando"
    }

    return (
        <div className={`${styles.tvCamara} cor-fundo2 ${classeDaCamara[props.estado.toLowerCase()]}`}>
            <div className={styles.tvCamaraFonteNumCamara}>
                <p className="txt-tv1">{props.numero} - {props.atividade.toUpperCase()}</p>
            </div>
            <p className="txt-tv2">{props.estado.toUpperCase()}</p>
            <p className="txt-tv2">
                {nomeAtendido !== "" && `${numeroAtendido + 1}. ${nomeAtendido}`}
                {nomeDupla !== "" && ` & ${nomeDupla}`}
                {numeroAtendido === "" && "CÂMARA VAZIA"}
            </p>
        </div>
    )
}

export default Tv