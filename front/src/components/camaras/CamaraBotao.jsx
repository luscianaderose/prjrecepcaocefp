import styles from "./CamaraBotao.module.css"
import axios from "axios"

function CamaraBotao (props) {
    const abrirCamara = async () => {
        const resposta = await axios.get(`http://127.0.0.1:5001/abrir_camara/${props.numero}`)
        window.location.reload()
    }

    const chamarProximo = async () => {
        const resposta = await axios.get(`http://127.0.0.1:5001/chamar_proximo/${props.numero}`)
        window.location.reload()
    }

    const avisar = async () => {
        const resposta = await axios.get(`http://127.0.0.1:5001/avisado/${props.numero}`)
        window.location.reload()
    }

    const fecharCamara = async () => {
        const resposta = await axios.get(`http://127.0.0.1:5001/fechar_camara/${props.numero}`)
        window.location.reload()
    }

    const estadoAcoes = {
        "fechada":{
            "acao":abrirCamara,
            "descricao":"ABRIR CÂMARA"
        },
        "atendendo":{
            "acao":chamarProximo,
            "descricao":"CHAMAR PRÓXIMO"
        },
        "último":{
            "acao":avisar,
            "descricao":"AVISEI QUE É O ÚLTIMO!"
        },
        "foi avisado":{
            "acao":fecharCamara,
            "descricao":"FECHAR CÂMARA"
        }
    }

    return (
        <button type="button">
            <a 
                className={`${styles.btCamara} a`} 
                onClick={estadoAcoes[props.estado.toLowerCase()]["acao"]}
                // href={`/abrir_camara/${props.numero}`}
            >
                {estadoAcoes[props.estado.toLowerCase()]["descricao"]}
            </a>
        </button>

    )
}

export default CamaraBotao