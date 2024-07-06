import styles from "./CamaraBotao.module.css"
import axios from "axios"
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

function CamaraBotao (props) {
    const abrirCamara = async () => {
        const resposta = await axios.get(`http://127.0.0.1:5001/abrir_camara/${props.numero}`)
        window.location.reload()
    }

    const chamarProximo = async () => {
        const audio = new Audio(audiosCamara[props.numero])
        audio.play()
        const resposta = await axios.get(`http://127.0.0.1:5001/chamar_proximo/${props.numero}`)
        console.log("props.numero, audiosCamara[props.numero]", props.numero, audiosCamara[props.numero])
        // window.location.reload()
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