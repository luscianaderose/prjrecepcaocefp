import styles from "./CamaraIcone.module.css"

function CamaraIcone (props) {
    const estadoAcoes = {
        "fechada":{
            "descricao":"FECHADA",
            "icone":styles.iconeFechada
        },
        "atendendo":{
            "descricao":"ATENDENDO",
            "icone":styles.iconeAtendendo
        },
        "último":{
            "descricao":"ÚLTIMO",
            "icone":styles.iconeAvisar
        },
        "foi avisado":{
            "descricao":"FOI AVISADO",
            "icone":styles.iconeAvisado
        }
    }
    // console.log("camara icone", props.estado.toLowerCase())
    return (
        <>
            <span className={estadoAcoes[props.estado.toLowerCase()]["icone"]}></span>
            {estadoAcoes[props.estado.toLowerCase()]["descricao"]}
            <br></br>
        </>
    )
}

export default CamaraIcone